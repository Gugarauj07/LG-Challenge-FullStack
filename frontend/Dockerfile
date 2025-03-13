FROM node:18 as build

WORKDIR /app

# Copiar arquivos de dependência
COPY package*.json ./

# Instalar dependências
RUN npm ci

# Copiar o código fonte
COPY . .

# Construir a aplicação - usando a configuração de produção
RUN npm run build -- --configuration=production --output-hashing=all --optimization --progress=false

# Segunda etapa - usar Nginx para servir o frontend
FROM nginx:alpine

# Variável de ambiente para porta (Cloud Run define automaticamente a PORT)
ENV PORT=8080

# Copiar os arquivos de build para o diretório de conteúdo do Nginx
COPY --from=build /app/dist/movielens-app /usr/share/nginx/html

# Copiar configuração personalizada do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor a porta 8080
EXPOSE 8080

# Iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]