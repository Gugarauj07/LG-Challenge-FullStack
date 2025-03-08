import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { environment } from '../../environments/environment';
import { Movie, MovieList, MovieStats } from '../models/movie.model';

@Injectable({
  providedIn: 'root'
})
export class MovieService {
  private apiUrl = `${environment.apiUrl}/movies`;

  constructor(private http: HttpClient) { }

  // Buscar filmes por título, ano e/ou gênero
  searchMovies(
    title?: string,
    year?: number,
    genre?: string,
    page: number = 0,
    limit: number = 10
  ): Observable<MovieList> {
    let params = new HttpParams()
      .set('skip', (page * limit).toString())
      .set('limit', limit.toString());

    if (title) params = params.set('title', title);
    if (year) params = params.set('year', year.toString());
    if (genre) params = params.set('genre', genre);

    return this.http.get<MovieList>(`${this.apiUrl}/search`, { params })
      .pipe(
        catchError(error => {
          console.error('Erro ao buscar filmes:', error);
          throw error;
        })
      );
  }

  // Obter filme por ID
  getMovieById(movieId: number): Observable<Movie> {
    return this.http.get<Movie>(`${this.apiUrl}/by-id/${movieId}`)
      .pipe(
        catchError(error => {
          console.error(`Erro ao obter filme ID ${movieId}:`, error);
          throw error;
        })
      );
  }

  // Obter os filmes mais bem avaliados
  getTopRatedMovies(limit: number = 10): Observable<Movie[]> {
    const params = new HttpParams().set('limit', limit.toString());

    return this.http.get<Movie[]>(`${this.apiUrl}/top-rated`, { params })
      .pipe(
        catchError(error => {
          console.error('Erro ao obter filmes mais bem avaliados:', error);
          throw error;
        })
      );
  }

  // Obter estatísticas de filmes
  getMovieStats(): Observable<MovieStats> {
    return this.http.get<MovieStats>(`${this.apiUrl}/stats`)
      .pipe(
        catchError(error => {
          console.error('Erro ao obter estatísticas de filmes:', error);
          throw error;
        })
      );
  }

  // Obter recomendações de filmes similares
  getSimilarMovies(movieId: number, limit: number = 6): Observable<Movie[]> {
    const params = new HttpParams().set('limit', limit.toString());

    return this.http.get<Movie[]>(`${environment.apiUrl}/recommendations/similar/${movieId}`, { params })
      .pipe(
        catchError(error => {
          console.error(`Erro ao obter filmes similares ao ID ${movieId}:`, error);
          throw error;
        })
      );
  }

  // Obter recomendações personalizadas para o usuário
  getUserRecommendations(limit: number = 10): Observable<Movie[]> {
    const params = new HttpParams().set('limit', limit.toString());

    return this.http.get<Movie[]>(`${environment.apiUrl}/recommendations/user`, { params })
      .pipe(
        catchError(error => {
          console.error('Erro ao obter recomendações personalizadas:', error);
          throw error;
        })
      );
  }

  // Obter URL da imagem do filme do TMDB (se disponível)
  getTMDBImageUrl(movie: Movie): string | null {
    if (!movie.tmdb_id) {
      return null;
    }
    return `https://image.tmdb.org/t/p/w500/${movie.tmdb_id}`;
  }

  // Obter link para o IMDB
  getIMDBLink(movie: Movie): string | null {
    if (!movie.imdb_id) {
      return null;
    }
    return `https://www.imdb.com/title/tt${movie.imdb_id}`;
  }
}