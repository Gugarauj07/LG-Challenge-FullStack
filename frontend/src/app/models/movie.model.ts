export interface Movie {
  id: number;
  title: string;
  year?: number;
  genres: string[];
  average_rating?: number;
  rating_count?: number;
}

export interface MovieStats {
  total_movies: number;
  total_ratings: number;
  average_rating: number;
  top_genres: {
    name: string;
    movie_count: number;
  }[];
}