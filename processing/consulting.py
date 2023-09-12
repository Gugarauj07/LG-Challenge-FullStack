import sqlite3

conn = sqlite3.connect('movielens.db')

cursor = conn.cursor()

title = "The Shawshank Redemption"
cursor.execute("SELECT * FROM movies WHERE title = 'Toy Story (1995)'")
movies = cursor.fetchall()

for movie in movies:
    print(movie)

cursor.close()
conn.close()