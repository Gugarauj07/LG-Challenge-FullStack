export interface Genre {
  id: number;
  name: string;
}

export interface Movie {
  id: number;
  movie_id: number;
  title: string;
  year?: number;
  imdb_id?: string;
  tmdb_id?: string;
  genres: Genre[];
  average_rating: number;
  rating_count: number;
}

export interface MovieList {
  items: Movie[];
  total: number;
}

export interface MovieStats {
  total_movies: number;
  total_ratings: number;
  average_rating: number;
  top_genres: { name: string; movie_count: number }[];
}