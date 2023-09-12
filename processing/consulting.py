import sqlite3

conn = sqlite3.connect('../movielens.db')

cursor = conn.cursor()

cursor.execute("SELECT * FROM movies")
movies = cursor.fetchall()

for movie in movies:
    print(movie)

cursor.close()
conn.close()