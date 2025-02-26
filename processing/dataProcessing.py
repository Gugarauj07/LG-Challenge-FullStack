import pandas as pd
import sqlite3
import math

print("Iniciando processamento dos dados")

def popularity_heuristic(row):
    return row['mean'] * math.sqrt(row['count'])

movies_df = pd.read_csv('./ml-25m/movies.csv')
ratings_df = pd.read_csv('./ml-25m/ratings.csv')
genomeScores_df = pd.read_csv('./ml-25m/genome-scores.csv')
genomeTags_df = pd.read_csv('./ml-25m/genome-tags.csv')
tags_df = pd.read_csv('./ml-25m/tags.csv')
links_df = pd.read_csv('./ml-25m/links.csv')

movies_df['year'] = movies_df['title'].str.extract(r'\((\d{4})\)$')
movies_df['title'] = movies_df['title'].str.replace(r'\(\d{4}\)', '', regex=True).str.strip()
# print(movies_df['title'])

average_ratings = ratings_df.groupby('movieId')['rating'].agg(['mean', 'count']).reset_index()
average_ratings['popularity_score'] = average_ratings.apply(popularity_heuristic, axis=1)
# print(average_ratings)

conn = sqlite3.connect('../movielens.db')

movies_df.to_sql('movies', conn, if_exists='replace', index=False)
ratings_df.to_sql('ratings', conn, if_exists='replace', index=False)
average_ratings.to_sql('avgRatings', conn, if_exists='replace', index=False)
genomeScores_df.to_sql('genomeScores', conn, if_exists='replace', index=False)
genomeTags_df.to_sql('genomeTags', conn, if_exists='replace', index=False)
tags_df.to_sql('tags', conn, if_exists='replace', index=False)
links_df.to_sql('links', conn, if_exists='replace', index=False)

conn.close()