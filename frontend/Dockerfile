FROM node:18 as build

WORKDIR /app

# Copiar arquivos de dependência
COPY package*.json ./

# Instalar dependências
RUN npm ci

# Copiar o código fonte
COPY . .

# Construir a aplicação
RUN npm run build

# Segunda etapa - usar Nginx para servir o frontend
FROM nginx:alpine

# Copiar os arquivos de build para o diretório de conteúdo do Nginx
COPY --from=build /app/dist/movielens-app /usr/share/nginx/html

# Copiar configuração personalizada do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor a porta 80
EXPOSE 80

# Iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]