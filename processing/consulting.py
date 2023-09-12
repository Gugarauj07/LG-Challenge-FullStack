import sqlite3

conn = sqlite3.connect('../movielens.db')

cursor = conn.cursor()

cursor.execute("""SELECT m.movieId, m.title, r.mean AS avg_rating, r.count AS num_rating
                            FROM movies as m
                            LEFT JOIN avgRatings AS r ON m.movieId = r.movieId
                            ORDER BY mean DESC
                            LIMIT 100;""")

movies = cursor.fetchall()

for movie in movies:
    print(movie)

cursor.close()
conn.close()