FROM python:3.11-slim

WORKDIR /app

# Copiar os arquivos de dependências
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código
COPY . .

# Variável de ambiente para porta (Cloud Run define automaticamente a PORT)
ENV PORT=8000

# Expor a porta que a aplicação usa
EXPOSE ${PORT}

# Comando para iniciar a aplicação
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}