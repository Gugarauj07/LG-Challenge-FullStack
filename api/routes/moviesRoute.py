from flask import Blueprint, jsonify, request
import sqlite3

movies_bp = Blueprint('movies', __name__)

# Teste: /movies?title=Toy Story
# Teste: /movies?year=1995&genres=Adventure

@movies_bp.route('/movies', methods=['GET'])
def list_movies_by_title():
    title = request.args.get('title')
    year = request.args.get('year')
    genre = request.args.get('genres')
    print(year, genre)

    if not title and not year and not genre:
        return jsonify({'error': 'Parameter is required'}), 400

    conn = sqlite3.connect('../movielens.db')
    cursor = conn.cursor()

    if title:
        cursor.execute('SELECT * FROM movies WHERE title LIKE ?', ('%' + title + '%',))
    elif year and genre:
        cursor.execute('SELECT * FROM movies WHERE year = ? AND genres LIKE ?', (year, ('%'+genre+'%')))

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

