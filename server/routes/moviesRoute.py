from flask import Blueprint, jsonify, request
import sqlite3

movies_bp = Blueprint('movies', __name__)

# Teste: /movies?title=Toy Story
# Teste: /movies?year=1995&genres=Adventure
# Teste: /movies?top=10

@movies_bp.route('/movies', methods=['GET'])
def list_movies_by_title():
    title = request.args.get('title')
    year = request.args.get('year')
    genre = request.args.get('genres')
    top = request.args.get('top')
    print(top)

    if not title and not year and not genre and not top:
        return jsonify({'error': 'Parameter is required'}), 400

    conn = sqlite3.connect('../movielens.db')
    cursor = conn.cursor()

    if title:
        cursor.execute('SELECT * FROM movies WHERE title LIKE ?', ('%' + title + '%',))
    elif year and genre:
        cursor.execute('SELECT * FROM movies WHERE year = ? AND genres LIKE ?', (year, ('%'+genre+'%')))
    elif top:
        # SELECT m.title, AVG(r.rating) AS avg_rating FROM movies AS m LEFT JOIN ratings AS r ON m.movieId = r.movieId GROUP BY m.title ORDER BY avg_rating DESC LIMIT 10;
        cursor.execute(f"""SELECT m.movieId, m.title, r.mean AS avg_rating, r.count AS num_rating, r.popularity_score
                            FROM movies as m
                            LEFT JOIN avgRatings AS r ON m.movieId = r.movieId
                            ORDER BY popularity_score DESC
                            LIMIT {top};""")

    movies = cursor.fetchall()

    conn.close()

    movie_list = []
    for movie in movies:
        movie_dict = {
            'id': movie[0],
            'title': movie[1],
            'avg_rating' if top else 'year': movie[2],
        }
        if top:
            movie_dict.update({
                'num_rated': movie[3],
                'popularity_score': movie[4]
            })
        movie_list.append(movie_dict)
    return jsonify(movie_list)

