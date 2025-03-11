import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, of, catchError } from 'rxjs';
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
    // Só carrega favoritos se houver um token
    if (localStorage.getItem('token')) {
      this.loadFavorites();
    }
  }

  // Carregar favoritos do usuário
  loadFavorites(): void {
    this.http.get<Movie[]>(this.apiUrl)
      .pipe(
        catchError(err => {
          console.error('Erro ao carregar favoritos:', err);
          return of([]);
        })
      )
      .subscribe(favorites => {
        this.favoritesSubject.next(favorites);
      });
  }

  // Obter favoritos
  getFavorites(): Observable<Movie[]> {
    return this.http.get<Movie[]>(this.apiUrl)
      .pipe(
        tap(favorites => {
          this.favoritesSubject.next(favorites);
        }),
        catchError(err => {
          console.error('Erro ao obter favoritos:', err);
          return of([]);
        })
      );
  }

  // Adicionar filme aos favoritos
  addToFavorites(movieId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${movieId}`, {})
      .pipe(
        tap(() => this.loadFavorites()),
        catchError(err => {
          console.error('Erro ao adicionar favorito:', err);
          return of(null);
        })
      );
  }

  // Remover filme dos favoritos
  removeFromFavorites(movieId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${movieId}`)
      .pipe(
        tap(() => this.loadFavorites()),
        catchError(err => {
          console.error('Erro ao remover favorito:', err);
          return of(null);
        })
      );
  }

  // Verificar se um filme está nos favoritos
  isFavorite(movieId: number): boolean {
    const favorites = this.favoritesSubject.value;
    return favorites.some(movie => movie.id === movieId);
  }
}