import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Movie } from '../models/movie.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RecommendationService {
  private apiUrl = `${environment.apiUrl}/recommendations`;

  constructor(private http: HttpClient) { }

  getUserRecommendations(limit: number = 10): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${this.apiUrl}/user`, {
      params: new HttpParams().set('limit', limit.toString())
    });
  }

  getSimilarMovies(movieId: number, limit: number = 10): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${this.apiUrl}/similar/${movieId}`, {
      params: new HttpParams().set('limit', limit.toString())
    });
  }
}