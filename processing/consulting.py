import sqlite3

conn = sqlite3.connect('../movielens.db')

cursor = conn.cursor()
title="Toy Story"

cursor.execute("""
    SELECT m.*, r.*
    FROM movies m
    LEFT JOIN avgRatings r ON m.movieId = r.movieId
    WHERE m.title LIKE ?
""", ('%' + title + '%',))
# cursor.execute('SELECT * FROM movies WHERE title LIKE ?', ('%' + title + '%',))


movies = cursor.fetchall()

for movie in movies:
    print(movie)

cursor.close()
conn.close()