from flask import Blueprint, jsonify, request
import sqlite3

movies_bp = Blueprint('movies', __name__)

# Teste: /movies?title=SeuTituloAqui

@movies_bp.route('/movies', methods=['GET'])
def list_movies_by_title():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Title parameter is required'}), 400

    conn = sqlite3.connect('.../../movielens.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM movies WHERE title LIKE ?', ('%' + title + '%',))
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

