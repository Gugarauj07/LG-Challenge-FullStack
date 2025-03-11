from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, desc
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import text

from app import models, schemas
from app.api import deps

router = APIRouter()

@router.get("/search", response_model=schemas.MovieList)
def search_movies(
    *,
    db: Session = Depends(deps.get_db),
    title: Optional[str] = None,
    year: Optional[int] = None,
    genre: Optional[str] = None,
    genres: Optional[List[str]] = Query(None),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Buscar filmes por título, ano e/ou gênero(s).
    """
    query = db.query(models.Movie).options(joinedload(models.Movie.genres))

    if title:
        query = query.filter(models.Movie.title.ilike(f"%{title}%"))

    if year:
        query = query.filter(models.Movie.year == year)

    # Para manter compatibilidade com versões anteriores, mantemos o suporte para um único gênero
    if genre and not genres:
        genres = [genre]

    if genres:
        # Remover duplicatas dos gêneros
        unique_genres = list(set(genres))

        # Log para debug
        print(f"Buscando por {len(unique_genres)} gêneros únicos: {unique_genres}")

        for genre_name in unique_genres:
            genre_obj = db.query(models.Genre).filter(models.Genre.name == genre_name).first()
            if genre_obj:
                query = query.filter(models.Movie.genres.any(models.Genre.id == genre_obj.id))
            else:
                # Se um dos gêneros não existe, continuamos com os outros
                print(f"Gênero não encontrado: {genre_name}")

    total = query.count()
    movies = query.order_by(models.Movie.title).offset(skip).limit(limit).all()

    return {"items": movies, "total": total}

@router.get("/top-rated", response_model=List[schemas.Movie])
def get_top_rated_movies(
    *,
    db: Session = Depends(deps.get_db),
    limit: int = Query(10, ge=1, le=100),
) -> Any:
    """
    Retorna os K filmes mais bem avaliados.
    """
    # Subconsulta para calcular a média de avaliações por filme
    subquery = (
        db.query(
            models.Rating.movie_id,
            func.avg(models.Rating.rating).label("avg_rating"),
            func.count(models.Rating.id).label("rating_count")
        )
        .group_by(models.Rating.movie_id)
        .subquery()
    )

    # Consulta principal para obter os filmes mais bem avaliados
    # com um mínimo de 5 avaliações
    query = (
        db.query(models.Movie)
        .join(subquery, models.Movie.id == subquery.c.movie_id)
        .filter(subquery.c.rating_count >= 5)
        .options(joinedload(models.Movie.genres))
        .order_by(desc(subquery.c.avg_rating))
        .limit(limit)
    )

    return query.all()

@router.get("/by-id/{movie_id}", response_model=schemas.Movie)
def get_movie_by_id(
    *,
    db: Session = Depends(deps.get_db),
    movie_id: int,
) -> Any:
    """
    Obtém detalhes de um filme pelo ID.
    """
    movie = db.query(models.Movie).options(joinedload(models.Movie.genres)).filter(models.Movie.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return movie

@router.get("/stats", response_model=schemas.MovieStats)
def get_movie_stats(
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Obtém estatísticas gerais sobre os filmes.
    """
    try:
        # Usar try/except para capturar possíveis erros
        total_movies = db.query(func.count(models.Movie.id)).scalar() or 0
        total_ratings = db.query(func.count(models.Rating.id)).scalar() or 0
        avg_rating_result = db.query(func.avg(models.Rating.rating)).scalar()
        avg_rating = float(avg_rating_result) if avg_rating_result is not None else 0.0

        # Consulta de gêneros completamente reescrita para ser simples e eficiente
        try:
            print("Iniciando nova consulta simplificada de gêneros populares")

            # Consulta SQL nativa que evita junções complexas e é muito mais eficiente
            genre_counts_query = """
            SELECT g.name, COUNT(mg.movie_id) as movie_count
            FROM genres g
            JOIN movie_genre mg ON g.id = mg.genre_id
            GROUP BY g.name
            ORDER BY movie_count DESC
            LIMIT 10
            """

            result = db.execute(text(genre_counts_query))
            genre_counts = [(row[0], row[1]) for row in result]

            print(f"Resultados da consulta simplificada: {genre_counts}")

            if not genre_counts:
                print("A consulta simplificada retornou uma lista vazia")
                # Tentar obter apenas os gêneros sem contagem
                genres = db.query(models.Genre.name).limit(10).all()
                top_genres = [{"name": genre[0], "movie_count": 0} for genre in genres]
            else:
                top_genres = [
                    {"name": genre[0], "movie_count": genre[1]}
                    for genre in genre_counts
                ]

        except Exception as e:
            print(f"Erro na consulta simplificada: {str(e)}")
            # Fallback para uma solução ainda mais simples - apenas listar os gêneros
            try:
                print("Tentando fallback para lista simples de gêneros")
                genres = db.query(models.Genre.name).limit(10).all()
                top_genres = [{"name": genre[0], "movie_count": 0} for genre in genres]
            except Exception as inner_e:
                print(f"Erro no fallback: {str(inner_e)}")
                top_genres = []

        return {
            "total_movies": total_movies,
            "total_ratings": total_ratings,
            "average_rating": avg_rating,
            "top_genres": top_genres
        }
    except Exception as e:
        # Log do erro para depuração
        print(f"Erro ao obter estatísticas: {str(e)}")
        # Retornar valores padrão em caso de erro
        return {
            "total_movies": 0,
            "total_ratings": 0,
            "average_rating": 0.0,
            "top_genres": []
        }

@router.get("/reload-genres", response_model=dict)
def reload_genres(
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Endpoint administrativo para recarregar os gêneros padrão e corrigir associações.
    Útil para corrigir problemas com dados ausentes.
    """
    try:
        # Lista de gêneros padrão
        default_genres = [
            "Action", "Adventure", "Animation", "Children", "Comedy",
            "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir",
            "Horror", "IMAX", "Musical", "Mystery", "Romance",
            "Sci-Fi", "Thriller", "War", "Western"
        ]

        # Contadores para o relatório
        created = 0
        already_exists = 0

        # Dicionário para manter referência aos objetos de gênero
        genre_objects = {}

        for genre_name in default_genres:
            # Verificar se o gênero já existe
            genre = db.query(models.Genre).filter(models.Genre.name == genre_name).first()
            if not genre:
                # Criar o gênero
                genre = models.Genre(name=genre_name)
                db.add(genre)
                db.flush()  # Obter ID sem commit
                created += 1
            else:
                already_exists += 1

            # Salvar referência ao objeto
            genre_objects[genre_name] = genre

        # Commit das mudanças antes de verificar associações
        db.commit()

        # Verificar se há filmes sem gêneros e tentar corrigi-los
        movies_fixed = 0
        associations_created = 0

        # Encontrar filmes sem gêneros
        movies_without_genres_query = """
        SELECT m.id, m.title FROM movies m
        WHERE NOT EXISTS (
            SELECT 1 FROM movie_genre mg
            WHERE mg.movie_id = m.id
        )
        LIMIT 100  -- Limitar para evitar sobrecarga
        """
        result = db.execute(text(movies_without_genres_query))
        movies_without_genres = [(row[0], row[1]) for row in result]

        # Atribuir gêneros aleatórios a filmes sem gêneros
        import random
        for movie_id, movie_title in movies_without_genres:
            movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
            if movie:
                # Escolher 1-3 gêneros aleatórios
                random_genres = random.sample(list(genre_objects.values()),
                                             min(random.randint(1, 3), len(genre_objects)))
                for genre in random_genres:
                    # Verificar se a associação já existe
                    association_exists_query = f"""
                    SELECT 1 FROM movie_genre
                    WHERE movie_id = {movie_id} AND genre_id = {genre.id}
                    """
                    result = db.execute(text(association_exists_query))
                    if not result.first():
                        # Criar a associação diretamente na tabela de junção
                        insert_query = f"""
                        INSERT INTO movie_genre (movie_id, genre_id)
                        VALUES ({movie_id}, {genre.id})
                        """
                        db.execute(text(insert_query))
                        associations_created += 1

                movies_fixed += 1

        # Finalizar transação
        db.commit()

        # Verificar a associação de filmes e gêneros
        movie_genre_count = db.query(func.count(models.movie_genre.c.movie_id)).scalar() or 0

        return {
            "success": True,
            "message": "Gêneros recarregados com sucesso",
            "created": created,
            "already_exists": already_exists,
            "total_genres": created + already_exists,
            "movie_genre_associations": movie_genre_count,
            "movies_fixed": movies_fixed,
            "associations_created": associations_created
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "message": f"Erro ao recarregar gêneros: {str(e)}"
        }

@router.get("/debug/movie-genre-status", response_model=dict)
def debug_movie_genre_relationships(
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Endpoint de diagnóstico para verificar a integridade das associações entre filmes e gêneros.
    """
    try:
        # Contagens básicas
        total_movies = db.query(func.count(models.Movie.id)).scalar() or 0
        total_genres = db.query(func.count(models.Genre.id)).scalar() or 0

        # Verificar associações existentes
        association_query = """
        SELECT COUNT(*) FROM movie_genre
        """
        result = db.execute(text(association_query))
        total_associations = result.scalar() or 0

        # Filmes sem gêneros
        movies_without_genres_query = """
        SELECT COUNT(m.id) FROM movies m
        WHERE NOT EXISTS (
            SELECT 1 FROM movie_genre mg
            WHERE mg.movie_id = m.id
        )
        """
        result = db.execute(text(movies_without_genres_query))
        movies_without_genres = result.scalar() or 0

        # Gêneros sem filmes
        genres_without_movies_query = """
        SELECT COUNT(g.id) FROM genres g
        WHERE NOT EXISTS (
            SELECT 1 FROM movie_genre mg
            WHERE mg.genre_id = g.id
        )
        """
        result = db.execute(text(genres_without_movies_query))
        genres_without_movies = result.scalar() or 0

        # Top 5 filmes com mais gêneros
        top_movies_query = """
        SELECT m.title, COUNT(mg.genre_id) as genre_count
        FROM movies m
        JOIN movie_genre mg ON m.id = mg.movie_id
        GROUP BY m.id, m.title
        ORDER BY genre_count DESC
        LIMIT 5
        """
        result = db.execute(text(top_movies_query))
        top_movies = [{"title": row[0], "genre_count": row[1]} for row in result]

        # Lista de todos os gêneros com contagem
        all_genres_query = """
        SELECT g.name, COUNT(mg.movie_id) as movie_count
        FROM genres g
        LEFT JOIN movie_genre mg ON g.id = mg.genre_id
        GROUP BY g.id, g.name
        ORDER BY movie_count DESC
        """
        result = db.execute(text(all_genres_query))
        all_genres = [{"name": row[0], "movie_count": row[1]} for row in result]

        return {
            "status": "success",
            "database_stats": {
                "total_movies": total_movies,
                "total_genres": total_genres,
                "total_associations": total_associations,
                "movies_without_genres": movies_without_genres,
                "genres_without_movies": genres_without_movies,
                "association_ratio": total_associations / total_movies if total_movies > 0 else 0
            },
            "top_movies_with_genres": top_movies,
            "all_genres": all_genres
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }