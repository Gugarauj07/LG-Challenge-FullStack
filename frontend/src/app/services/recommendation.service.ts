import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { Movie } from '../models/movie.model';
import { environment } from '../../environments/environment';
import { ApiConfigService } from './api-config.service';

@Injectable({
  providedIn: 'root'
})
export class RecommendationService {
  private apiUrl: string;

  constructor(
    private http: HttpClient,
    private apiConfigService: ApiConfigService
  ) {
    this.apiUrl = `${this.apiConfigService.getApiUrl()}/recommendations`;
    console.log('RecommendationService usando API URL:', this.apiUrl);
  }

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