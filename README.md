# MovieLens - Sistema de Recomendação de Filmes

Este projeto implementa um sistema completo de recomendação de filmes utilizando o dataset MovieLens. O sistema consiste em um backend em FastAPI que processa os dados e disponibiliza endpoints REST, e um frontend em Angular que permite aos usuários interagir com esses dados de forma intuitiva.

## 📌 Links de Deploy

- **Frontend:** [https://movielens-frontend-d6sxdenlgq-uc.a.run.app](https://movielens-frontend-d6sxdenlgq-uc.a.run.app)
- **Backend API:** [https://movielens-backend-d6sxdenlgq-uc.a.run.app](https://movielens-backend-d6sxdenlgq-uc.a.run.app)
- **API Docs (Swagger):** [https://movielens-backend-d6sxdenlgq-uc.a.run.app/docs](https://movielens-backend-d6sxdenlgq-uc.a.run.app/docs)

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
- Frontend: http://localhost:4200
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

Acesse o frontend em: http://localhost:4200

### Deploy no Google Cloud Run

O projeto inclui um script de deploy automático para o Google Cloud Run:

```bash
# Certifique-se de ter o Google Cloud SDK instalado e configurado
chmod +x deploy-cloud-run.sh
./deploy-cloud-run.sh
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

### Processamento de Dados

- Os dados do MovieLens são processados durante a inicialização do aplicativo
- ETL automatizado para carregar, limpar e transformar dados
- Normalização de tabelas para eficiência e escalabilidade
- Índices para acelerar consultas frequentes

### Sistema de Recomendação

O sistema implementa dois tipos de recomendação:

1. **Filtragem Colaborativa**
   - Recomendações baseadas no comportamento de usuários semelhantes
   - Utiliza matriz de similaridade de cosseno para identificar padrões

2. **Filtragem Baseada em Conteúdo**
   - Recomendações baseadas em características dos filmes (gêneros, atores, etc.)
   - Utiliza TF-IDF para análise de similaridade entre filmes

### Segurança

- Autenticação JWT para proteção de endpoints sensíveis
- Hashing de senhas com bcrypt
- CORS configurado para aceitar apenas origens específicas
- Rate limiting para prevenir ataques de força bruta

### Implantação e DevOps

- Containerização com Docker para garantir consistência entre ambientes
- CI/CD com GitHub Actions (opcional)
- Deploy no Google Cloud Run para escalabilidade automática
- Nginx como proxy reverso para o frontend

## 📌 Principais Desafios e Soluções

### Problema de Cross-Origin em Produção

Um dos principais desafios foi configurar corretamente o proxy reverso no Nginx para o ambiente de produção. A solução implementada:

1. Configuração do environment.prod.ts para apontar para a URL absoluta da API em produção
2. Simplificação do ApiConfigService para usar diretamente o valor do environment.ts
3. Configuração do Nginx para servir a aplicação Angular corretamente

### Otimização de Consultas

Para garantir boa performance mesmo com grande volume de dados:

1. Índices estrategicamente criados nas colunas mais consultadas
2. Consultas SQL otimizadas com joins eficientes
3. Paginação implementada em todos os endpoints que retornam listas

### Gestão de Estado no Frontend

Implementamos um serviço de estado global usando RxJS para:

1. Compartilhar dados entre componentes sem prop drilling
2. Armazenar em cache resultados de consultas frequentes
3. Gerenciar o estado de autenticação e informações do usuário

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

### Técnicas

1. **Migração para GraphQL**
   - Implementar GraphQL para consultas mais flexíveis e eficientes
   - Reduzir o overfetching e underfetching de dados

2. **Cache Distribuído**
   - Implementar Redis para cache distribuído e melhorar a performance
   - Armazenar resultados de consultas frequentes e sessões de usuário

3. **Testes Automatizados Abrangentes**
   - Aumentar a cobertura de testes unitários e de integração
   - Implementar testes end-to-end com Cypress ou Playwright

4. **Análise de Telemetria**
   - Implementar logging estruturado e monitoramento com ELK Stack ou similar
   - Rastrear padrões de uso para otimizar a experiência do usuário

5. **Progressive Web App (PWA)**
   - Converter o frontend para PWA para permitir uso offline e melhorar a experiência móvel

## 📌 Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📌 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## 📌 Contato

Gustavo Araujo - [@Gugarauj07](https://github.com/Gugarauj07)
