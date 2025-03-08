import numpy as np
from typing import List, Dict, Tuple
from sqlalchemy import func
from sqlalchemy.orm import Session
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from app import models

# Cache para evitar recalcular as matrizes frequentemente
user_item_matrix_cache = None
item_similarity_matrix_cache = None
last_update_timestamp = 0

def _build_user_item_matrix(db: Session) -> Tuple[pd.DataFrame, Dict[int, int], Dict[int, int]]:
    """
    Constrói a matriz de usuários x filmes para calcular recomendações
    """
    # Obter todas as avaliações
    ratings = db.query(
        models.Rating.user_id,
        models.Rating.movie_id,
        models.Rating.rating
    ).all()

    # Converter para DataFrame
    df = pd.DataFrame(ratings, columns=['user_id', 'movie_id', 'rating'])

    # Criar mapeamentos para IDs de usuários e filmes
    unique_user_ids = df['user_id'].unique()
    unique_movie_ids = df['movie_id'].unique()

    user_to_idx = {user_id: idx for idx, user_id in enumerate(unique_user_ids)}
    movie_to_idx = {movie_id: idx for idx, movie_id in enumerate(unique_movie_ids)}
    idx_to_movie = {idx: movie_id for movie_id, idx in movie_to_idx.items()}

    # Criar matriz esparsa para usuários x filmes
    matrix = np.zeros((len(unique_user_ids), len(unique_movie_ids)))

    for _, row in df.iterrows():
        user_idx = user_to_idx[row['user_id']]
        movie_idx = movie_to_idx[row['movie_id']]
        matrix[user_idx, movie_idx] = row['rating']

    # Normalizar as avaliações (subtrair a média de cada usuário)
    user_means = np.true_divide(matrix.sum(1), (matrix != 0).sum(1))
    normalized_matrix = matrix.copy()

    for i in range(matrix.shape[0]):
        normalized_matrix[i, matrix[i] != 0] -= user_means[i]

    return normalized_matrix, user_to_idx, idx_to_movie

def _calculate_item_similarity(matrix: np.ndarray) -> np.ndarray:
    """
    Calcula a matriz de similaridade entre os filmes
    """
    # Transpor a matriz para calcular similaridade entre filmes (não usuários)
    item_matrix = matrix.T

    # Substituir NaN por 0 (após a transposição)
    item_matrix = np.nan_to_num(item_matrix)

    # Calcular similaridade de cosseno entre os filmes
    similarity = cosine_similarity(item_matrix)

    # Definir a diagonal principal como 0 para evitar recomendar o mesmo filme
    np.fill_diagonal(similarity, 0)

    return similarity

def get_recommendations_for_user(db: Session, user_id: int, limit: int = 10) -> List[int]:
    """
    Gera recomendações de filmes para um usuário específico usando filtragem colaborativa
    """
    global user_item_matrix_cache, item_similarity_matrix_cache, last_update_timestamp

    # Verificar se precisamos atualizar o cache
    latest_rating_timestamp = db.query(func.max(models.Rating.timestamp)).scalar() or 0
    if latest_rating_timestamp > last_update_timestamp or user_item_matrix_cache is None:
        # Reconstruir as matrizes
        user_item_matrix, user_to_idx, idx_to_movie = _build_user_item_matrix(db)
        item_similarity_matrix = _calculate_item_similarity(user_item_matrix)

        # Atualizar o cache
        user_item_matrix_cache = (user_item_matrix, user_to_idx, idx_to_movie)
        item_similarity_matrix_cache = item_similarity_matrix
        last_update_timestamp = latest_rating_timestamp
    else:
        # Usar o cache
        user_item_matrix, user_to_idx, idx_to_movie = user_item_matrix_cache
        item_similarity_matrix = item_similarity_matrix_cache

    # Obter avaliações do usuário
    try:
        user_idx = user_to_idx[user_id]
    except KeyError:
        # Usuário não encontrado na matriz, usar recomendações populares
        top_movies = db.query(
            models.Rating.movie_id,
            func.avg(models.Rating.rating).label('avg_rating'),
            func.count(models.Rating.id).label('rating_count')
        ).group_by(models.Rating.movie_id).order_by(
            func.avg(models.Rating.rating).desc(),
            func.count(models.Rating.id).desc()
        ).limit(limit).all()

        return [movie[0] for movie in top_movies]

    # Filmes que o usuário já avaliou
    user_ratings = user_item_matrix[user_idx]
    rated_items = np.where(user_ratings != 0)[0]

    # Calcular pontuações de recomendação
    recommendation_scores = np.zeros(user_ratings.shape)

    for item_idx in range(user_ratings.shape[0]):
        # Pular filmes que o usuário já avaliou
        if item_idx in rated_items:
            continue

        # Calcular a pontuação de predição
        for rated_item in rated_items:
            recommendation_scores[item_idx] += user_ratings[rated_item] * item_similarity_matrix[rated_item, item_idx]

    # Obter os índices dos filmes com maiores pontuações
    top_item_indices = np.argsort(recommendation_scores)[::-1][:limit]

    # Converter índices de volta para IDs de filmes
    recommended_movie_ids = [idx_to_movie[idx] for idx in top_item_indices]

    return recommended_movie_ids

def get_similar_movies(db: Session, movie_id: int, limit: int = 10) -> List[int]:
    """
    Encontra filmes similares a um filme específico
    """
    global user_item_matrix_cache, item_similarity_matrix_cache, last_update_timestamp

    # Verificar se precisamos atualizar o cache
    latest_rating_timestamp = db.query(func.max(models.Rating.timestamp)).scalar() or 0
    if latest_rating_timestamp > last_update_timestamp or user_item_matrix_cache is None:
        # Reconstruir as matrizes
        user_item_matrix, user_to_idx, idx_to_movie = _build_user_item_matrix(db)
        item_similarity_matrix = _calculate_item_similarity(user_item_matrix)

        # Atualizar o cache
        user_item_matrix_cache = (user_item_matrix, user_to_idx, idx_to_movie)
        item_similarity_matrix_cache = item_similarity_matrix
        last_update_timestamp = latest_rating_timestamp
    else:
        # Usar o cache
        user_item_matrix, _, idx_to_movie = user_item_matrix_cache
        item_similarity_matrix = item_similarity_matrix_cache

    # Mapear movie_id para o índice na matriz
    movie_to_idx = {v: k for k, v in idx_to_movie.items()}

    try:
        movie_idx = movie_to_idx[movie_id]
    except KeyError:
        # Filme não encontrado, retornar filmes populares
        top_movies = db.query(
            models.Rating.movie_id,
            func.avg(models.Rating.rating).label('avg_rating'),
            func.count(models.Rating.id).label('rating_count')
        ).group_by(models.Rating.movie_id).order_by(
            func.avg(models.Rating.rating).desc(),
            func.count(models.Rating.id).desc()
        ).limit(limit).all()

        return [movie[0] for movie in top_movies]

    # Obter os índices dos filmes mais similares
    similar_movie_indices = np.argsort(item_similarity_matrix[movie_idx])[::-1][:limit]

    # Converter índices de volta para IDs de filmes
    similar_movie_ids = [idx_to_movie[idx] for idx in similar_movie_indices]

    return similar_movie_ids