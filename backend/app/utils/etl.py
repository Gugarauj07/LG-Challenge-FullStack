import os
import threading
import logging
import urllib.request
import zipfile
import tempfile
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import func, select, text

from app import models
from app.utils.data_import import import_movielens_data
from app.database.session import engine, Base

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.etl")

# Flag global para controlar se o ETL já foi executado nesta instância
etl_executed = False
etl_lock = threading.Lock()

# URL padrão para o dataset MovieLens
MOVIELENS_URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

def is_database_empty(db: Session) -> bool:
    """
    Verifica se o banco de dados está vazio (sem filmes carregados).
    """
    try:
        movie_count = db.query(func.count(models.Movie.id)).scalar()
        return movie_count == 0
    except Exception as e:
        logger.error(f"Erro ao verificar se o banco de dados está vazio: {e}")
        # Se ocorrer um erro, assume que precisamos inicializar
        return True

def is_database_initialized() -> bool:
    """
    Verifica se o banco de dados já foi inicializado (tabelas criadas).
    """
    try:
        # Tenta executar uma consulta simples para verificar se as tabelas existem
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='movies'"))
            return result.scalar() is not None
    except Exception as e:
        logger.error(f"Erro ao verificar se o banco de dados está inicializado: {e}")
        return False

def setup_database():
    """
    Cria as tabelas no banco de dados.
    """
    logger.info("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tabelas criadas com sucesso.")

def download_movielens_data(url=MOVIELENS_URL, target_dir=None):
    """
    Baixa o dataset MovieLens e o extrai para o diretório alvo.

    Args:
        url: URL para baixar o dataset
        target_dir: Diretório de destino. Se None, usa o diretório padrão.

    Returns:
        Caminho para o diretório com os dados extraídos
    """
    # Determinar o diretório de destino
    if target_dir is None:
        # Caminho padrão relativo ao diretório raiz do projeto
        root_dir = Path(__file__).parent.parent.parent.parent  # backend/app/utils/etl.py -> backend/
        target_dir = os.path.join(root_dir, "data")

    # Garantir que o diretório de destino existe
    os.makedirs(target_dir, exist_ok=True)

    extract_dir = os.path.join(target_dir, "ml-latest-small")

    # Verificar se os dados já existem
    if os.path.exists(extract_dir) and os.path.isdir(extract_dir):
        logger.info(f"Dataset já existe em {extract_dir}. Pulando download.")
        return extract_dir

    # Baixar e extrair o dataset
    logger.info(f"Baixando dataset MovieLens de {url}...")

    # Criar arquivo temporário para o download
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_file:
        temp_path = temp_file.name
        try:
            # Baixar o arquivo
            urllib.request.urlretrieve(url, temp_path)

            # Extrair o arquivo
            logger.info(f"Extraindo dataset para {target_dir}...")
            with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                zip_ref.extractall(target_dir)

            logger.info("Download e extração concluídos com sucesso.")
            return extract_dir
        except Exception as e:
            logger.error(f"Erro ao baixar ou extrair dataset: {e}")
            raise
        finally:
            # Limpar arquivo temporário
            if os.path.exists(temp_path):
                os.unlink(temp_path)

def run_etl(data_dir=None, download_if_missing=True):
    """
    Executa o processo de ETL, carregando os dados do MovieLens para o banco de dados.

    Args:
        data_dir: Diretório contendo os arquivos do MovieLens. Se None, usa o diretório padrão.
        download_if_missing: Se True, baixa os dados se não forem encontrados localmente.
    """
    global etl_executed

    # Usar lock para garantir que apenas uma thread executará o ETL
    with etl_lock:
        # Verificar se o ETL já foi executado nesta instância
        if etl_executed:
            logger.info("ETL já foi executado nesta instância da aplicação.")
            return

        # Verificar se o banco de dados está inicializado
        if not is_database_initialized():
            logger.info("Banco de dados não inicializado. Criando tabelas...")
            setup_database()

        # Verificar se os dados já foram carregados
        db = Session(engine)
        try:
            if not is_database_empty(db):
                logger.info("Banco de dados já contém dados. Pulando ETL.")
                etl_executed = True
                return

            # Determinar o diretório de dados
            if data_dir is None:
                # Caminho padrão relativo ao diretório raiz do projeto
                root_dir = Path(__file__).parent.parent.parent.parent  # backend/app/utils/etl.py -> backend/
                data_dir = os.path.join(root_dir, "data", "ml-latest-small")

            # Verificar se o diretório de dados existe
            if not os.path.exists(data_dir):
                if download_if_missing:
                    logger.info(f"Diretório de dados não encontrado: {data_dir}")
                    logger.info("Baixando dataset MovieLens...")
                    data_dir = download_movielens_data()
                else:
                    logger.error(f"Diretório de dados não encontrado: {data_dir}")
                    logger.error("Por favor, verifique se os dados do MovieLens foram baixados corretamente.")
                    return

            # Importar dados
            logger.info(f"Iniciando ETL com dados de: {data_dir}")
            import_movielens_data(data_dir)

            etl_executed = True
            logger.info("ETL concluído com sucesso.")
        except Exception as e:
            logger.error(f"Erro durante o ETL: {e}")
        finally:
            db.close()

def init_app_data():
    """
    Função a ser chamada na inicialização da aplicação para carregar os dados.
    """
    # Executar ETL em uma thread separada para não bloquear a inicialização da aplicação
    threading.Thread(target=run_etl, kwargs={"download_if_missing": True}).start()
    logger.info("Processo ETL iniciado em segundo plano.")

if __name__ == "__main__":
    # Para execução independente
    run_etl(download_if_missing=True)