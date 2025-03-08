#!/usr/bin/env python
"""
Script para testar a função de recomendações de filmes similares diretamente.
"""
import os
import sys
import logging
from pathlib import Path

# Configurar o logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("recommendation-test")

# Adicionar o diretório do projeto ao PATH para importações
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_similar_movies(movie_id=1, limit=5):
    """Testar a função get_similar_movies diretamente."""
    from sqlalchemy.orm import Session
    from app.database.session import engine
    from app.services.recommendation import get_similar_movies

    # Criar sessão do banco de dados
    db = Session(engine)

    try:
        # Verificar se o filme existe
        from app.models.movie import Movie
        movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()

        if not movie:
            logger.error(f"Filme com movie_id={movie_id} não encontrado!")
            return

        logger.info(f"Encontrado filme: {movie.title} (ID={movie.id}, movie_id={movie.movie_id})")
        logger.info(f"Gêneros: {', '.join(g.name for g in movie.genres)}")

        # Chamar diretamente a função de recomendação com debug detalhado
        logger.info(f"Chamando get_similar_movies para movie_id={movie_id}...")
        similar_movie_ids = get_similar_movies(db, movie_id, limit)

        if not similar_movie_ids:
            logger.warning("Nenhum filme similar encontrado!")
            return

        logger.info(f"Encontrados {len(similar_movie_ids)} filmes similares")

        # Exibir detalhes dos filmes similares
        similar_movies = db.query(Movie).filter(Movie.id.in_(similar_movie_ids)).all()

        for i, movie in enumerate(similar_movies, 1):
            logger.info(f"{i}. {movie.title} (ID={movie.id}, movie_id={movie.movie_id})")
            logger.info(f"   Gêneros: {', '.join(g.name for g in movie.genres)}")

    except Exception as e:
        logger.exception(f"Erro durante o teste: {e}")
    finally:
        db.close()

def test_alternative_recommendation(movie_id=1, limit=5):
    """
    Implementar uma abordagem alternativa baseada apenas em gêneros
    para verificar se conseguimos gerar recomendações.
    """
    from sqlalchemy.orm import Session
    from sqlalchemy import func
    from app.database.session import engine
    from app.models.movie import Movie, Genre, movie_genre

    # Criar sessão do banco de dados
    db = Session(engine)

    try:
        # Verificar se o filme existe
        movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()

        if not movie:
            logger.error(f"Filme com movie_id={movie_id} não encontrado!")
            return

        logger.info(f"Encontrado filme: {movie.title} (ID={movie.id}, movie_id={movie.movie_id})")
        logger.info(f"Gêneros: {', '.join(g.name for g in movie.genres)}")

        # Obter gêneros do filme
        genre_ids = [genre.id for genre in movie.genres]

        # Encontrar filmes com gêneros semelhantes
        similar_genre_movies = (
            db.query(Movie)
            .join(movie_genre)
            .filter(movie_genre.c.genre_id.in_(genre_ids))
            .filter(Movie.id != movie.id)  # Excluir o próprio filme
            .group_by(Movie.id)
            .order_by(func.count().desc())  # Ordenar por número de gêneros em comum
            .limit(limit)
        ).all()

        logger.info(f"Encontrados {len(similar_genre_movies)} filmes similares por gênero")

        # Exibir detalhes dos filmes similares
        for i, movie in enumerate(similar_genre_movies, 1):
            logger.info(f"{i}. {movie.title} (ID={movie.id}, movie_id={movie.movie_id})")
            logger.info(f"   Gêneros: {', '.join(g.name for g in movie.genres)}")

    except Exception as e:
        logger.exception(f"Erro durante o teste: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Testar recomendações de filmes similares')
    parser.add_argument('--movie-id', type=int, default=1,
                        help='ID do filme para buscar similares (padrão: 1)')
    parser.add_argument('--limit', type=int, default=5,
                        help='Número de filmes similares para retornar (padrão: 5)')
    parser.add_argument('--alt', action='store_true',
                        help='Usar implementação alternativa baseada apenas em gêneros')

    args = parser.parse_args()

    if args.alt:
        test_alternative_recommendation(args.movie_id, args.limit)
    else:
        test_similar_movies(args.movie_id, args.limit)