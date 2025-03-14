# MovieLens - Sistema de Recomendação de Filmes

## 📌 Links de Deploy

- **Frontend:** [https://movielens-frontend-d6sxdenlgq-uc.a.run.app](https://movielens-frontend-d6sxdenlgq-uc.a.run.app)
- **Backend API:** [https://movielens-backend-d6sxdenlgq-uc.a.run.app](https://movielens-backend-d6sxdenlgq-uc.a.run.app)
- **API Docs (Swagger):** [https://movielens-backend-d6sxdenlgq-uc.a.run.app/docs](https://movielens-backend-d6sxdenlgq-uc.a.run.app/docs)

## ⚠️ Aviso Importante sobre o Deploy

O sistema implantado no Google Cloud Run não está totalmente funcional no momento. Devido a limitações de tempo e configuração, o download automático do dataset MovieLens não está funcionando corretamente no ambiente de deploy.

Como o processo de deploy no Cloud Run demora um tempo considerável, não foi possível finalizar a implementação desta funcionalidade específica antes do prazo. O sistema funciona perfeitamente em ambiente local (via Docker ou execução direta), onde o download e processamento do dataset ocorrem automaticamente.

Para uma experiência completa, recomendo executar o projeto localmente seguindo as instruções abaixo.

## 📌 Guia de Instalação e Uso

### Requisitos

- Docker e Docker Compose
- Git
- Node.js 18+ e npm (para desenvolvimento local)
- Python 3.11+ (para desenvolvimento local)

### Clonando o Repositório

```bash
git clone https://github.com/Gugarauj07/LG-Challenge-FullStack.git
cd LG-Challenge-FullStack
```

### Execução com Docker Compose (Recomendado)

O método mais fácil para executar a aplicação completa é usando Docker Compose:

```bash
docker-compose up --build -d
```

Após a inicialização, acesse:
- Frontend: http://localhost/home
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Execução Local (Sem Docker)

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
ng serve
```
## 📌 Explicação Técnica

### Arquitetura do Sistema

O projeto utiliza uma arquitetura de microsserviços, com frontend e backend desacoplados:

- **Frontend (Angular 15)**
  - Utiliza Angular Material para componentes de UI
  - Implementa reactive forms para manipulação de formulários
  - Interceptors HTTP para gerenciamento de tokens e manipulação de erros
  - Lazy loading de módulos para melhor performance
  - Angular Guards para proteção de rotas

- **Backend (FastAPI)**
  - API REST com documentação automática (Swagger)
  - Autenticação JWT para proteção de endpoints
  - SQLAlchemy para ORM e interação com banco de dados
  - Pydantic para validação de dados e schemas
  - Integração com scikit-learn para algoritmos de recomendação

### Escolha do FastAPI para o Backend

Um dos principais diferenciais que motivou a escolha do FastAPI para este projeto de recomendação de filmes foi sua integração perfeita com ecossistemas de ciência de dados. O FastAPI permite importar e utilizar bibliotecas como scikit-learn, pandas e NumPy diretamente no código da API, sem necessidade de microsserviços separados para processamento de dados ou inferência de modelos. Esta característica é especialmente valiosa para sistemas de recomendação, que dependem de algoritmos estatísticos e processamento de dados em tempo real.

### Processamento de Dados

- Os dados do MovieLens são processados durante a inicialização do aplicativo
- ETL automatizado para carregar, limpar e transformar dados
- Normalização de tabelas para eficiência e escalabilidade
- Índices para acelerar consultas frequentes

### Sistema de Recomendação

O sistema de recomendação implementado combina técnicas avançadas de machine learning para oferecer sugestões personalizadas aos usuários. Ao invés de utilizar uma única abordagem, o sistema integra duas metodologias complementares que trabalham em conjunto para gerar recomendações mais precisas e diversificadas.

A primeira metodologia implementada é a Filtragem Colaborativa, que funciona sob o princípio de que usuários com históricos de preferências semelhantes provavelmente terão gostos similares no futuro. O algoritmo analisa padrões nas avaliações de milhares de usuários para identificar estas similaridades. Utilizando técnicas de álgebra linear, especificamente a similaridade de cosseno entre vetores de avaliações, o sistema consegue identificar usuários com perfis semelhantes e recomendar filmes que foram bem avaliados por estes "vizinhos próximos", mas que ainda não foram vistos pelo usuário atual. Esta abordagem é particularmente eficaz para descobrir conteúdo que talvez não seja óbvio baseado apenas nos gêneros preferidos do usuário.

Complementarmente, o sistema também emprega a Filtragem Baseada em Conteúdo, que analisa as características intrínsecas dos filmes – como gêneros, diretores, atores e palavras-chave – para identificar similaridades temáticas e estilísticas entre obras. Esta técnica utiliza representações vetoriais das características dos filmes, processadas através do algoritmo TF-IDF (Term Frequency-Inverse Document Frequency), que pondera a importância relativa de cada atributo. Quando um usuário demonstra interesse por determinados filmes, o sistema consegue recomendar obras com perfil semelhante, mesmo que estas não tenham sido avaliadas por muitos usuários, contornando assim o problema de "cold start" comum em sistemas baseados apenas em filtragem colaborativa.

A combinação destas duas abordagens permite que o sistema ofereça recomendações mais robustas e contextualizadas, equilibrando a descoberta de novos conteúdos com a precisão baseada em preferências já expressas pelo usuário. Os algoritmos são executados de forma eficiente graças à integração com a biblioteca scikit-learn, que implementa versões otimizadas destes métodos de aprendizado de máquina.

## 📌 Melhorias Futuras

### Funcionais

1. **Sistema de Avaliação em Tempo Real**
   - Permitir que usuários avaliem filmes e vejam atualizações imediatas nas recomendações

2. **Integração com APIs Externas**
   - Incorporar dados adicionais de APIs como TMDB ou OMDB para enriquecer informações dos filmes
   - Adicionar trailers, pôsteres em alta resolução e links para serviços de streaming

3. **Recomendações Personalizadas Avançadas**
   - Implementar algoritmos de deep learning para recomendações mais precisas
   - Incorporar fatores temporais (filmes assistidos recentemente têm mais peso)

4. **Recursos Sociais**
   - Permitir que usuários compartilhem listas e recomendações
   - Criar grupos de discussão sobre filmes

