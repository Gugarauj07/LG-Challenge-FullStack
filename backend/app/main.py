from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.api import api_router
from app.core.config import settings
from app.utils.etl import init_app_data

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para o projeto MovieLens Challenge",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, deve-se limitar aos domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do MovieLens Challenge. Acesse /docs para a documentação da API."}

@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da aplicação."""
    logger.info("Iniciando a aplicação...")
    init_app_data()  # Iniciar ETL em segundo plano

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)