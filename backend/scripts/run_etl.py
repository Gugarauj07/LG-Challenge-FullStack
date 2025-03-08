#!/usr/bin/env python
"""
Script para executar o ETL manualmente.
Este script importa os dados do MovieLens para o banco de dados.
"""
import os
import sys
import argparse
import logging

# Configurar o logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("etl-manual")

# Adicionar o diretório do projeto ao PATH para importações
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Função principal para executar o ETL."""
    from app.utils.etl import run_etl

    parser = argparse.ArgumentParser(description='Executar ETL do MovieLens')
    parser.add_argument('--data-dir', type=str, default=None,
                        help='Diretório com os dados do MovieLens (se omitido, usa o diretório padrão)')
    parser.add_argument('--download', action='store_true',
                        help='Baixar dados se não forem encontrados localmente')
    parser.add_argument('--force', action='store_true',
                        help='Forçar reimportação mesmo se o banco já contiver dados')

    args = parser.parse_args()

    if args.force:
        logger.warning("Reimportação forçada solicitada. Esta operação pode demorar.")
        # Código extra para limpar o banco de dados pode ser adicionado aqui,
        # mas isso pode ser implementado posteriormente se necessário

    logger.info("Iniciando ETL...")
    run_etl(data_dir=args.data_dir, download_if_missing=args.download)
    logger.info("Processo ETL concluído!")

if __name__ == "__main__":
    main()