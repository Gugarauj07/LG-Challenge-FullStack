from flask import Blueprint, jsonify
import sqlite3

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/movies')
def list_movies():
    conn = sqlite3.connect('.../../movielens.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()

    conn.close()

    movie_list = []
    for movie in movies:
        movie_dict = {
            'id': movie[0],
            'title': movie[1],
            'year': movie[2],
        }
        movie_list.append(movie_dict)
    return jsonify(movie_list)

@movies_bp.route('/movies/<int:movie_id>')
def get_movie(movie_id):
    # Coloque o código para obter um filme específico aqui
    return jsonify({'message': f'Movie with ID {movie_id}'})

