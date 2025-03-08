import csv
import os
import re
from typing import Dict, List, Set, Tuple

import pandas as pd
from sqlalchemy.orm import Session

from app import models
from app.database.session import Base, engine

def extract_year_from_title(title: str) -> Tuple[str, int]:
    """
    Extrai o ano do título do filme, se disponível.
    Retorna o título limpo e o ano.
    """
    year_pattern = r'(\(\d{4}\))$'
    match = re.search(year_pattern, title)

    if match:
        year_str = match.group(1).strip('()')
        cleaned_title = title[:match.start()].strip()
        return cleaned_title, int(year_str)

    return title, None

def import_movies(db: Session, movies_file: str) -> Dict[int, int]:
    """
    Importa os filmes do arquivo CSV para o banco de dados.
    Retorna um mapeamento de movie_id original para id do banco de dados.
    """
    print("Importando filmes...")

    # Mapear nomes de gêneros para objetos Genre
    genre_map = {}

    # Mapear movie_id original para id do banco
    movie_id_map = {}

    with open(movies_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Extrair o ano do título
            title, year = extract_year_from_title(row['title'])

            # Criar ou obter gêneros
            genres = row['genres'].split('|')
            genre_objects = []

            for genre_name in genres:
                if genre_name == '(no genres listed)':
                    continue

                if genre_name not in genre_map:
                    genre = db.query(models.Genre).filter(models.Genre.name == genre_name).first()
                    if not genre:
                        genre = models.Genre(name=genre_name)
                        db.add(genre)
                        db.flush()  # Para obter o ID
                    genre_map[genre_name] = genre

                genre_objects.append(genre_map[genre_name])

            # Verificar se o filme já existe
            movie = db.query(models.Movie).filter(models.Movie.movie_id == int(row['movieId'])).first()

            if not movie:
                # Criar novo filme
                movie = models.Movie(
                    movie_id=int(row['movieId']),
                    title=title,
                    year=year,
                    genres=genre_objects
                )
                db.add(movie)
                db.flush()  # Para obter o ID

            movie_id_map[int(row['movieId'])] = movie.id

    db.commit()
    print(f"Importados {len(movie_id_map)} filmes e {len(genre_map)} gêneros.")
    return movie_id_map

def import_links(db: Session, links_file: str, movie_id_map: Dict[int, int]) -> None:
    """
    Importa os links para IMDb e TMDb do arquivo CSV.
    """
    print("Importando links externos...")

    with open(links_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            movie_id = int(row['movieId'])

            if movie_id in movie_id_map:
                db_id = movie_id_map[movie_id]
                movie = db.query(models.Movie).filter(models.Movie.id == db_id).first()

                if movie:
                    movie.imdb_id = row.get('imdbId')
                    movie.tmdb_id = row.get('tmdbId')

    db.commit()
    print("Links importados com sucesso.")

def import_ratings(db: Session, ratings_file: str, movie_id_map: Dict[int, int]) -> Dict[int, int]:
    """
    Importa as avaliações do arquivo CSV.
    Retorna um mapeamento de user_id original para id do banco de dados.
    """
    print("Importando avaliações...")

    # Mapear user_id original para id do banco
    user_id_map = {}
    rating_count = 0

    # Ler em chunks para evitar problemas de memória
    for chunk in pd.read_csv(ratings_file, chunksize=10000):
        for _, row in chunk.iterrows():
            user_id = int(row['userId'])
            movie_id = int(row['movieId'])

            # Verificar se o usuário já existe no mapeamento
            if user_id not in user_id_map:
                # Verificar se o usuário já existe no banco
                user = db.query(models.User).filter(models.User.id == user_id).first()
                if not user:
                    # Criar usuário do sistema de avaliação
                    username = f"user_{user_id}"
                    email = f"user_{user_id}@example.com"
                    password_hash = "hashed_placeholder_password"  # Placeholder

                    user = models.User(
                        id=user_id,
                        username=username,
                        email=email,
                        hashed_password=password_hash,
                        is_active=True
                    )
                    db.add(user)
                    db.flush()

                user_id_map[user_id] = user.id

            # Verificar se o filme existe no mapeamento
            if movie_id in movie_id_map:
                db_movie_id = movie_id_map[movie_id]

                # Verificar se a avaliação já existe
                existing_rating = db.query(models.Rating).filter(
                    models.Rating.user_id == user_id_map[user_id],
                    models.Rating.movie_id == db_movie_id
                ).first()

                if not existing_rating:
                    # Criar nova avaliação
                    rating = models.Rating(
                        user_id=user_id_map[user_id],
                        movie_id=db_movie_id,
                        rating=float(row['rating']),
                        timestamp=int(row['timestamp'])
                    )
                    db.add(rating)
                    rating_count += 1

                    # Commit a cada 1000 avaliações para evitar transações muito grandes
                    if rating_count % 1000 == 0:
                        db.commit()
                        print(f"Importadas {rating_count} avaliações...")

    db.commit()
    print(f"Importadas {rating_count} avaliações de {len(user_id_map)} usuários.")
    return user_id_map

def import_tags(db: Session, tags_file: str, movie_id_map: Dict[int, int], user_id_map: Dict[int, int]) -> None:
    """
    Importa as tags do arquivo CSV.
    """
    print("Importando tags...")

    tag_count = 0

    with open(tags_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            user_id = int(row['userId'])
            movie_id = int(row['movieId'])

            # Verificar se o usuário e o filme existem nos mapeamentos
            if user_id in user_id_map and movie_id in movie_id_map:
                db_user_id = user_id_map[user_id]
                db_movie_id = movie_id_map[movie_id]

                # Verificar se a tag já existe
                existing_tag = db.query(models.Tag).filter(
                    models.Tag.user_id == db_user_id,
                    models.Tag.movie_id == db_movie_id,
                    models.Tag.tag == row['tag']
                ).first()

                if not existing_tag:
                    # Criar nova tag
                    tag = models.Tag(
                        user_id=db_user_id,
                        movie_id=db_movie_id,
                        tag=row['tag'],
                        timestamp=int(row['timestamp'])
                    )
                    db.add(tag)
                    tag_count += 1

                    # Commit a cada 1000 tags para evitar transações muito grandes
                    if tag_count % 1000 == 0:
                        db.commit()
                        print(f"Importadas {tag_count} tags...")

    db.commit()
    print(f"Importadas {tag_count} tags.")

def import_movielens_data(data_dir: str) -> None:
    """
    Importa todos os dados do MovieLens para o banco de dados.
    """
    print("Iniciando importação dos dados do MovieLens...")

    # Criar as tabelas no banco de dados
    Base.metadata.create_all(bind=engine)

    # Arquivos de dados
    movies_file = os.path.join(data_dir, 'movies.csv')
    links_file = os.path.join(data_dir, 'links.csv')
    ratings_file = os.path.join(data_dir, 'ratings.csv')
    tags_file = os.path.join(data_dir, 'tags.csv')

    # Criar sessão do banco de dados
    db = Session(engine)

    try:
        # Importar dados em sequência
        movie_id_map = import_movies(db, movies_file)
        import_links(db, links_file, movie_id_map)
        user_id_map = import_ratings(db, ratings_file, movie_id_map)
        import_tags(db, tags_file, movie_id_map, user_id_map)

        print("Importação concluída com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"Erro durante a importação: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Caminho para o diretório de dados do MovieLens
    data_dir = "../data/ml-latest-small"
    import_movielens_data(data_dir)