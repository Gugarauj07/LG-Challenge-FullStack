import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, map } from 'rxjs';

import { Movie, MovieStats } from '../models/movie.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MovieService {
  private apiUrl = `${environment.apiUrl}/movies`;

  constructor(private http: HttpClient) { }

  getTopRated(limit: number = 10): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${this.apiUrl}/top-rated`, {
      params: new HttpParams().set('limit', limit.toString())
    });
  }

  searchMovies(query: { title?: string, year?: number, genre?: string, genres?: string[] }): Observable<Movie[]> {
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
      query.genres.forEach(genre => {
        params = params.append('genres', genre);
      });
    }

    return this.http.get<{items: Movie[], total: number}>(`${this.apiUrl}/search`, { params })
      .pipe(
        map(response => response.items)
      );
  }

  getMovieById(id: number): Observable<Movie> {
    return this.http.get<Movie>(`${this.apiUrl}/by-id/${id}`);
  }

  getMovieStats(): Observable<MovieStats> {
    return this.http.get<MovieStats>(`${this.apiUrl}/stats`);
  }
}