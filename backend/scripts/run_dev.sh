#!/bin/bash

# Ativar ambiente virtual
if [ -d "venv" ]; then
    echo "Ativando ambiente virtual..."
    source venv/bin/activate
fi

# Executar o servidor
echo "Iniciando o servidor FastAPI..."
PYTHONPATH=$PYTHONPATH:. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000