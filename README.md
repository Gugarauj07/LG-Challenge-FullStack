🛠️ Tecnologias Obrigatórias
Frontend: Angular 15
Backend: FastAPI
🎯 Objetivo
Você deve desenvolver um projeto utilizando o conjunto de dados MovieLens, cumprindo os seguintes desafios:

📊 Preparação e Processamento dos Dados
🌐 Disponibilização dos Dados via API
🖥️ Consumo da API em um Cliente Gráfico
🧠 Extra (Avançado) - Implementação de Algoritmos de Recomendação
1️⃣ Preparação e Processamento dos Dados
O primeiro objetivo é obter, processar e estruturar os dados para uso posterior.

📌 Tarefas:
Baixe o dataset MovieLens e analise sua estrutura.
https://grouplens.org/datasets/movielens/
Desenvolva um programa que leia os arquivos de entrada e crie uma base de dados organizada.
Armazene os dados em memória, arquivos ou banco de dados gerenciado (SQL ou NoSQL).
Limpe os dados, garantindo que inconsistências sejam tratadas.
Normalize as tabelas, garantindo eficiência e escalabilidade.
Gere índices para acelerar consultas nas próximas etapas.
📌 Desafio Adicional:
Implemente um pipeline de ETL (Extract, Transform, Load) para carregar e transformar os dados automaticamente ao iniciar a aplicação.
2️⃣ Disponibilização dos Dados via API
O segundo objetivo é implementar uma API RESTful que disponibilize os dados processados para consumo.

📌 Endpoints Obrigatórios:
Buscar filmes por título → Retorna todos os filmes que correspondem a um título específico ou parte dele.
Buscar filmes por ano e gênero → Retorna os filmes lançados em um determinado ano e que pertencem a um gênero específico.
Listar os K filmes mais bem avaliados → Retorna os melhores filmes ordenados por nota média de avaliação.
Login/Autenticação → Implementação de autenticação do usuário.
📌 Desafios Adicionais:
Filtrar filmes por popularidade → Desenvolva um algoritmo que leve em consideração a quantidade de avaliações e suas notas para definir a popularidade de um filme.
Criar um endpoint para estatísticas gerais → Exiba insights como número total de filmes, gêneros mais populares, média de avaliações por filme, etc.
Implementar autenticação na API → Garanta que apenas usuários autenticados possam acessar determinados endpoints.
3️⃣ Consumo dos Dados via Aplicação Cliente
O terceiro objetivo é desenvolver um cliente gráfico que consuma os endpoints da API e permita a interação dos usuários.

📌 Requisitos Mínimos:
Interface intuitiva para consultar filmes pelo título.
Filtros de busca avançados por ano e gênero.
Exibição do ranking dos melhores filmes.
Dashboard com estatísticas sobre filmes, gêneros mais populares e top usuários.
📌 Diferenciais:
Adicione funcionalidades como busca por atores/diretores (se os dados estiverem disponíveis).
Crie um sistema de favoritos para que os usuários salvem seus filmes preferidos.
Desenvolva um sistema de login e personalização da experiência do usuário.
Faça o deploy da aplicação em um ambiente acessível online (Heroku, AWS, Vercel, etc.).
4️⃣ Extra (Avançado) - Implementação de Algoritmos de Recomendação
Este é um desafio adicional para quem deseja demonstrar habilidades em Machine Learning e Data Science.

📌 Tarefa:
Implemente um sistema de recomendação de filmes utilizando técnicas como Filtragem Colaborativa, Baseada em Conteúdo ou Híbrida.
Utilize bibliotecas como Scikit-learn, TensorFlow, PyTorch ou outra de sua escolha.
Disponibilize um endpoint /recommendations que retorne sugestões de filmes com base no histórico do usuário.
📌 Diferenciais:
Aplique técnicas de aprendizado profundo para criar recomendações mais sofisticadas.
Otimize o desempenho utilizando caching e indexação eficiente.
✅ Critérios de Avaliação
Durante a avaliação, levaremos em conta os seguintes aspectos:

✅ Qualidade do Código → Código limpo, bem estruturado, seguindo boas práticas de programação.
✅ Documentação → Código bem documentado e instruções claras sobre como rodar o projeto.
✅ Desempenho → Consultas otimizadas para garantir boa performance.
✅ Escalabilidade → Solução pensada para lidar com grandes volumes de dados.
✅ Boas Práticas de Git → Histórico organizado, commits bem descritos e uso adequado de branches.
✅ Testes Automatizados → Cobertura de testes para garantir o bom funcionamento da aplicação.
✅ Deploy e Configuração → Facilidade de setup e execução da aplicação (preferencialmente Dockerizada).

📜 Entregáveis
Você deve fornecer os seguintes artefatos no seu repositório:

📌 Código-fonte completo da solução desenvolvida.
📌 Arquivos Docker para facilitar a execução do projeto.
📌 Guia de Instalação e Uso contendo instruções para configuração e execução da aplicação.
📌 Explicação técnica sobre as tecnologias escolhidas e decisões tomadas.
📌 Possíveis melhorias futuras que poderiam ser implementadas.

📌 Bônus: Caso tenha feito o deploy da API e/ou aplicação cliente, forneça os links no README.md.

📢 Dicas Finais
Facilite a execução → Certifique-se de que qualquer pessoa consiga rodar seu projeto seguindo os passos do guia.
Cuide do desempenho → Evite consultas lentas e garanta tempos de resposta rápidos.
Seja criativo → Diferenciais bem implementados são sempre bem-vindos!
Teste bem sua solução → Testes bem escritos demonstram profissionalismo e confiabilidade.
Siga boas práticas de segurança → Proteja a API e os dados de usuários.
