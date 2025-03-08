import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { CookieService } from 'ngx-cookie-service';

import { environment } from '../../environments/environment';
import { User, LoginRequest, RegisterRequest, AuthResponse } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;
  private currentUserSubject: BehaviorSubject<User | null>;
  public currentUser$: Observable<User | null>;
  private tokenKey = 'auth_token';

  constructor(
    private http: HttpClient,
    private cookieService: CookieService
  ) {
    this.currentUserSubject = new BehaviorSubject<User | null>(this.getUserFromStorage());
    this.currentUser$ = this.currentUserSubject.asObservable();
  }

  // Getter para obter o usuário atual
  public get currentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  // Login do usuário
  login(loginData: LoginRequest): Observable<User> {
    const formData = new FormData();
    formData.append('username', loginData.username);
    formData.append('password', loginData.password);

    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, formData)
      .pipe(
        tap(response => this.storeToken(response.access_token)),
        tap(() => this.loadCurrentUser()),
        map(() => this.currentUserValue as User),
        catchError(error => {
          console.error('Erro no login:', error);
          throw error;
        })
      );
  }

  // Registro de novo usuário
  register(userData: RegisterRequest): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/register`, userData)
      .pipe(
        catchError(error => {
          console.error('Erro no registro:', error);
          throw error;
        })
      );
  }

  // Carregar informações do usuário atual
  loadCurrentUser(): Observable<User | null> {
    if (!this.getToken()) {
      this.currentUserSubject.next(null);
      return of(null);
    }

    return this.http.get<User>(`${this.apiUrl}/me`)
      .pipe(
        tap(user => this.currentUserSubject.next(user)),
        catchError(() => {
          this.logout();
          return of(null);
        })
      );
  }

  // Logout do usuário
  logout(): void {
    this.cookieService.delete(this.tokenKey);
    localStorage.removeItem(this.tokenKey);
    this.currentUserSubject.next(null);
  }

  // Verificar se o usuário está logado
  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  // Obter o token de autenticação
  getToken(): string {
    return this.cookieService.get(this.tokenKey) || localStorage.getItem(this.tokenKey) || '';
  }

  // Armazenar o token de autenticação
  private storeToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
    this.cookieService.set(this.tokenKey, token, { path: '/' });
  }

  // Obter o usuário do armazenamento local
  private getUserFromStorage(): User | null {
    if (!this.getToken()) {
      return null;
    }

    // Tentar obter o usuário do localStorage, se existir
    const userJson = localStorage.getItem('current_user');
    if (userJson) {
      try {
        return JSON.parse(userJson);
      } catch {
        return null;
      }
    }
    return null;
  }
}