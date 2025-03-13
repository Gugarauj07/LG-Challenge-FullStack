import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, map, catchError, of } from 'rxjs';

import { Movie, MovieStats } from '../models/movie.model';
import { environment } from '../../environments/environment';
import { ApiConfigService } from './api-config.service';

@Injectable({
  providedIn: 'root'
})
export class MovieService {
  private apiUrl: string;

  constructor(
    private http: HttpClient,
    private apiConfigService: ApiConfigService
  ) {
    this.apiUrl = `${this.apiConfigService.getApiUrl()}/movies`;
    console.log('MovieService usando API URL:', this.apiUrl);
  }

  getTopRated(skip: number = 0, limit: number = 10): Observable<{items: Movie[], total: number}> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());

    return this.http.get<{items: Movie[], total: number}>(`${this.apiUrl}/top-rated`, { params })
      .pipe(
        catchError(error => {
          console.error('Erro ao carregar filmes mais bem avaliados:', error);
          return of({items: [], total: 0});
        })
      );
  }

  searchMovies(query: {
    title?: string,
    year?: number,
    genre?: string,
    genres?: string[],
    skip?: number,
    limit?: number
  }): Observable<{items: Movie[], total: number}> {
    let params = new HttpParams();

    if (query.title) {
      params = params.set('title', query.title);
    }

    if (query.year) {
      params = params.set('year', query.year.toString());
    }

    if (query.genre && !query.genres) {
      params = params.set('genre', query.genre);
    }

    if (query.genres && query.genres.length > 0) {
      const uniqueGenres = [...new Set(query.genres)];
      uniqueGenres.forEach(genre => {
        params = params.append('genres', genre);
      });
    }

    if (query.skip !== undefined) {
      params = params.set('skip', query.skip.toString());
    }

    if (query.limit !== undefined) {
      params = params.set('limit', query.limit.toString());
    }

    return this.http.get<{items: Movie[], total: number}>(`${this.apiUrl}/search`, { params })
      .pipe(
        catchError(error => {
          console.error('Erro ao buscar filmes:', error);
          return of({items: [], total: 0});
        })
      );
  }

  getMovieById(id: number): Observable<Movie> {
    return this.http.get<Movie>(`${this.apiUrl}/by-id/${id}`)
      .pipe(
        catchError(error => {
          console.error(`Erro ao carregar filme ${id}:`, error);
          return of({} as Movie);
        })
      );
  }

  getMovieStats(): Observable<MovieStats> {
    // Implementar um timeout mais longo para operações pesadas de estatísticas
    return this.http.get<MovieStats>(`${this.apiUrl}/stats`)
      .pipe(
        catchError(error => {
          console.error('Erro ao carregar estatísticas:', error);
          // Retornar um objeto de estatísticas vazio em caso de erro
          return of({
            total_movies: 0,
            total_ratings: 0,
            average_rating: 0,
            top_genres: []
          });
        })
      );
  }
}