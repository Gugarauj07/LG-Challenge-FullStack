# Preparando o ambiente

Usando Docker: 
- Execute no terminal: ```docker build -t challenge .``` 
- Execute no terminal: ```docker run -p 5000:5000 challenge``` 
- Abra seu navegador no endereço: http://127.0.0.1:5000

Se nao tiver docker:
- Certifique-se que tenha python instalado na sua máquina
- Execute o arquivo "setup.sh" no terminal: ```./setup.sh```
- Abra seu navegador no endereço: http://127.0.0.1:5000

# Explicando as tecnologias

Decidi usar a linguagem python, por ser mais prática tanto no processamento dos dados, quanto na implementação de REST APIs. 

## Primeira parte do desafio: Processamento de dados

Na primeira parte do desafio, fiz um script para automaticamente baixar e deszipar o dataset que foi provido. Com os dados em mãos, usei a biblioteca pandas para ler os arquivos .csv. 
Analisando os dados de movies.csv, percebi que a informação do ano de lançamento estava junto com o titulo, entao separei-os em colunas diferentes. Além disso, no arquivo ratings.csv havia muita repetição de dados, o que levaria a consultas mais demoradas no sql, entao processei os dados de rating para cada filme classificado, criando uma outra tabela que teria apenas sua média de rating e o número de vezes que foi classificado.
Após isso, criamos o banco de dados a partir desses arquivos csv, usando o banco SQLITE. Escolhi esta tecnologia por não precisar baixar nada para usá-la.

## Segunda parte do desafio: Deixando os dados disponíveis

Decidi usar o framework "Flask", pois necessita de poucas linhas de código para rodar uma API. Então, levantei a rota ```/movies``` que recebe os parâmetros: title, year, genre e top.
São feitas pesquisas em sql para filtrar os filmes por cada tipo de parâmetro dado. É retornado pela api um json com o id, titulo, genero, ano, rating, quantidade de ratings, e popularidade. 
A popularidade foi adicionada para levar em consideração não só os ratings, mas também a quantidade de classificações em cada filme. O cáuculo usado foi: ```rating médio x raiz quadrada da quantidade de classificações```. O parâmetro "top" leva em consideração a popularidade em ordem decrescente.
Teste: /movies?title=Toy Story
Teste: /movies?year=1995&genres=Adventure
Teste: /movies?top=10

## Terceira parte do desafio: Consumindo os dados

Como não precisamos de interfaces avançadas, decidi usar a biblioteca "Bootstrap" com o próprio flask para desenvolver o frontend.

![image](https://github.com/Gugarauj07/LG-Challenge-FullStack/assets/92393578/df6e3c5c-66a4-41e7-b0bd-4e9472823fda)
