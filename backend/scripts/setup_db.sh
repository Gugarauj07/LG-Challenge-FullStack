#!/bin/bash

# Ativar ambiente virtual
if [ -d "venv" ]; then
    echo "Ativando ambiente virtual..."
    source venv/bin/activate
fi

# Executar o script ETL diretamente
echo "Configurando banco de dados e importando dados..."
PYTHONPATH=$PYTHONPATH:. python -c "from app.utils.etl import run_etl; run_etl(download_if_missing=True)"

echo "Configuração concluída!"