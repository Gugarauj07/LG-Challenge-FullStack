FROM node:18 as build

WORKDIR /app

# Copiar arquivos de dependência
COPY package*.json ./

# Instalar dependências
RUN npm ci

# Copiar o código fonte
COPY . .

# Adicionar configuração para API URL
RUN echo "window.apiUrl = '${API_URL:-/api}';" > src/assets/config.js

# Construir a aplicação - adicionando flag --configuration=production para ignorar os warnings de orçamento
RUN npm run build -- --configuration=production --output-hashing=all --optimization --progress=false

# Segunda etapa - usar Nginx para servir o frontend
FROM nginx:alpine

# Variável de ambiente para porta (Cloud Run define automaticamente a PORT)
ENV PORT=8080

# Copiar os arquivos de build para o diretório de conteúdo do Nginx
COPY --from=build /app/dist/movielens-app /usr/share/nginx/html

# Copiar configuração personalizada do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Script para substituir a variável PORT no arquivo de configuração do Nginx e iniciar
RUN echo '#!/bin/sh' > /docker-entrypoint.sh && \
    echo 'echo "Iniciando o Nginx..."' >> /docker-entrypoint.sh && \
    echo 'exec nginx -g "daemon off;"' >> /docker-entrypoint.sh && \
    chmod +x /docker-entrypoint.sh

# Expor a porta 8080
EXPOSE 8080

# Usar o script de entrada personalizado
CMD ["/docker-entrypoint.sh"]