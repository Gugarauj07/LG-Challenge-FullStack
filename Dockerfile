# Use uma imagem base do Python
FROM python

# Crie um diretório de trabalho no contêiner
WORKDIR /app

COPY . /app

# Instale as dependências do Python
RUN pip install -r requirements.txt

# Mude para o diretório 'processing' e execute os scripts
WORKDIR /app/processing
RUN python downloading.py
RUN python dataProcessing.py

# Mude para o diretório 'server' e execute o aplicativo Flask
WORKDIR /app/server
CMD ["python", "app.py"]
