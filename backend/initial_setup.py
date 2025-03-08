"""
Script para inicializar o banco de dados e importar os dados do MovieLens.
Este script deve ser executado uma vez para configurar o ambiente.
"""
import os
import sys

# Adicionar o diretório do projeto ao PATH para importações
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import Base, engine
from app.utils.data_import import import_movielens_data

def setup_database():
    """
    Cria as tabelas no banco de dados.
    """
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso.")

def main():
    """
    Função principal para inicializar o banco de dados e importar os dados.
    """
    setup_database()

    # Caminho para o diretório de dados do MovieLens
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/ml-latest-small")

    if not os.path.exists(data_dir):
        print(f"Diretório de dados não encontrado: {data_dir}")
        print("Por favor, verifique se os dados do MovieLens foram baixados corretamente.")
        return

    # Importar dados
    import_movielens_data(data_dir)

if __name__ == "__main__":
    main()