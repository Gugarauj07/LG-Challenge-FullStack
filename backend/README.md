# Backend do MovieLens Challenge

Este é o backend do desafio MovieLens, desenvolvido com FastAPI, SQLAlchemy e sistemas de recomendação.

## Requisitos

- Python 3.9+
- Virtualenv
- Dataset MovieLens (baixado automaticamente durante a execução)

## Instalação

1. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o banco de dados e importe os dados:
```bash
./scripts/setup_db.sh
```

## Executando a Aplicação

```bash
./scripts/run_dev.sh
```

A API estará disponível em http://localhost:8000

Documentação OpenAPI: http://localhost:8000/docs

## Pipeline ETL Automático

O sistema possui um pipeline ETL que é executado automaticamente na inicialização da aplicação. Este pipeline:

1. Verifica se o banco de dados já está inicializado
2. Verifica se os dados já estão carregados
3. Se necessário, baixa automaticamente o dataset MovieLens
4. Importa e transforma os dados para o banco de dados

O ETL é executado em uma thread separada para não bloquear a inicialização da aplicação.

## Scripts Utilitários

- `scripts/run_dev.sh`: Inicia o servidor de desenvolvimento
- `scripts/setup_db.sh`: Configura o banco de dados e importa os dados
- `scripts/run_etl.py`: Permite executar o ETL manualmente com opções adicionais

## Executando o ETL Manualmente

Para executar o ETL manualmente, você pode usar o script `run_etl.py`:

```bash
# Execução básica
python scripts/run_etl.py

# Baixar dados se não existirem
python scripts/run_etl.py --download

# Especificar diretório de dados
python scripts/run_etl.py --data-dir /caminho/para/dados
```

## Estrutura do Projeto

```
backend/
├── app/
│   ├── api/            # Endpoints da API
│   ├── core/           # Configurações centrais
│   ├── database/       # Conexão com banco de dados
│   ├── models/         # Modelos SQLAlchemy
│   ├── schemas/        # Esquemas Pydantic
│   ├── services/       # Serviços (recomendação, etc.)
│   └── utils/          # Utilitários (ETL, importação, etc.)
├── scripts/            # Scripts utilitários
├── requirements.txt    # Dependências
└── README.md           # Esta documentação
```

## API Endpoints

- **Autenticação**: `/api/v1/auth/`
  - Login: `POST /login`
  - Registro: `POST /register`
  - Perfil: `GET /me`

- **Filmes**: `/api/v1/movies/`
  - Busca: `GET /search?title=&year=&genre=`
  - Top Avaliados: `GET /top-rated?limit=10`
  - Por ID: `GET /by-id/{movie_id}`
  - Estatísticas: `GET /stats`

- **Recomendações**: `/api/v1/recommendations/`
  - Para Usuário: `GET /user?limit=10`
  - Filmes Similares: `GET /similar/{movie_id}?limit=10` 