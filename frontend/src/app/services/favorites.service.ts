import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

import { Movie } from '../models/movie.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class FavoritesService {
  private apiUrl = `${environment.apiUrl}/favorites`;
  private favoritesSubject = new BehaviorSubject<Movie[]>([]);
  public favorites$ = this.favoritesSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadFavorites();
  }

  // Carregar favoritos do usuário
  loadFavorites(): void {
    this.http.get<Movie[]>(this.apiUrl).subscribe({
      next: (favorites) => {
        this.favoritesSubject.next(favorites);
      },
      error: (err) => {
        console.error('Erro ao carregar favoritos:', err);
      }
    });
  }

  // Obter favoritos
  getFavorites(): Observable<Movie[]> {
    return this.http.get<Movie[]>(this.apiUrl);
  }

  // Adicionar filme aos favoritos
  addToFavorites(movieId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${movieId}`, {}).pipe(
      tap(() => this.loadFavorites())
    );
  }

  // Remover filme dos favoritos
  removeFromFavorites(movieId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${movieId}`).pipe(
      tap(() => this.loadFavorites())
    );
  }

  // Verificar se um filme está nos favoritos
  isFavorite(movieId: number): boolean {
    const favorites = this.favoritesSubject.value;
    return favorites.some(movie => movie.id === movieId);
  }
}