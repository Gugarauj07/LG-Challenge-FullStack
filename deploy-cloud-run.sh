#!/bin/bash
# Script para implantar a aplicação MovieLens no Google Cloud Run

# Definir variáveis
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"  # Altere para a região desejada
BACKEND_IMAGE="gcr.io/$PROJECT_ID/movielens-backend"
FRONTEND_IMAGE="gcr.io/$PROJECT_ID/movielens-frontend"

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Função para verificar erros
check_error() {
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERRO: $1${NC}"
        exit 1
    fi
}

# 1. Verificar se o gcloud está instalado
echo -e "${GREEN}Verificando pré-requisitos...${NC}"
if ! command -v gcloud &> /dev/null; then
    echo "Google Cloud SDK (gcloud) não encontrado. Por favor, instale-o: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# 2. Verificar se o usuário está logado
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo "Você não está logado no Google Cloud SDK. Fazendo login..."
    gcloud auth login
    check_error "Falha ao fazer login no Google Cloud"
fi

# 3. Verificar se o projeto está configurado
if [ -z "$PROJECT_ID" ]; then
    echo "Nenhum projeto configurado. Por favor, configure um projeto:"
    gcloud projects list
    read -p "Digite o ID do projeto: " PROJECT_ID
    gcloud config set project $PROJECT_ID
    check_error "Falha ao configurar o projeto"
fi

# 4. Habilitar as APIs necessárias
echo -e "${GREEN}Habilitando APIs necessárias...${NC}"
gcloud services enable cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com containerregistry.googleapis.com
check_error "Falha ao habilitar as APIs necessárias"

# 5. Construir e enviar as imagens Docker para o Container Registry
echo -e "${GREEN}Construindo e enviando imagens Docker...${NC}"

echo "Construindo imagem do backend..."
cd backend
gcloud builds submit --tag $BACKEND_IMAGE . --timeout=15m
check_error "Falha ao construir a imagem do backend"
cd ..

echo "Construindo imagem do frontend..."
cd frontend
gcloud builds submit --tag $FRONTEND_IMAGE . --timeout=15m
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Aviso: Houve problemas ao construir a imagem do frontend.${NC}"
    echo -e "${YELLOW}Verifique os logs acima. Continuando apenas com o backend...${NC}"
    FRONTEND_FAILED=true
else
    FRONTEND_FAILED=false
fi
cd ..

# 6. Implantar o backend no Cloud Run
echo -e "${GREEN}Implantando backend no Cloud Run...${NC}"
gcloud run deploy movielens-backend \
    --image=$BACKEND_IMAGE \
    --platform=managed \
    --region=$REGION \
    --allow-unauthenticated
check_error "Falha ao implantar o backend no Cloud Run"

# 7. Obter a URL do backend para configurar o frontend
BACKEND_URL=$(gcloud run services describe movielens-backend --platform=managed --region=$REGION --format="value(status.url)")
echo "Backend implantado em: $BACKEND_URL"

# 8. Implantar o frontend no Cloud Run (apenas se não falhou)
if [ "$FRONTEND_FAILED" != "true" ]; then
    echo -e "${GREEN}Implantando frontend no Cloud Run...${NC}"
    gcloud run deploy movielens-frontend \
        --image=$FRONTEND_IMAGE \
        --platform=managed \
        --region=$REGION \
        --set-env-vars="API_URL=${BACKEND_URL}/api" \
        --allow-unauthenticated

    if [ $? -ne 0 ]; then
        echo -e "${RED}Falha ao implantar o frontend no Cloud Run.${NC}"
        FRONTEND_FAILED=true
    else
        # 9. Obter a URL do frontend
        FRONTEND_URL=$(gcloud run services describe movielens-frontend --platform=managed --region=$REGION --format="value(status.url)")
    fi
fi

# 10. Exibir as URLs de acesso
echo -e "${GREEN}Implantação concluída!${NC}"
echo -e "Backend: ${GREEN}$BACKEND_URL${NC}"
if [ "$FRONTEND_FAILED" != "true" ]; then
    echo -e "Frontend: ${GREEN}$FRONTEND_URL${NC}"
else
    echo -e "${YELLOW}Frontend: Não foi possível implantar. Apenas o backend está disponível.${NC}"
    echo -e "${YELLOW}Tente refazer a implantação do frontend depois de resolver os problemas.${NC}"
fi
echo -e "API Docs: ${GREEN}$BACKEND_URL/docs${NC}"