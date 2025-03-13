import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of, tap, catchError } from 'rxjs';
import { Router } from '@angular/router';

import { User, UserLogin, UserRegister, Token } from '../models/user.model';
import { environment } from '../../environments/environment';
import { ApiConfigService } from './api-config.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl: string;
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser = this.currentUserSubject.asObservable();
  private readonly TOKEN_KEY = 'auth_token';

  constructor(
    private http: HttpClient,
    private router: Router,
    private apiConfigService: ApiConfigService
  ) {
    this.apiUrl = `${this.apiConfigService.getApiUrl()}/auth`;
    console.log('AuthService usando API URL:', this.apiUrl);
    this.checkToken();
  }

  private checkToken(): void {
    const token = localStorage.getItem('token');
    if (token) {
      this.getProfile().pipe(
        // Se der erro, apenas limpa o token e retorna null, mas não causa redirecionamento
        catchError(() => {
          localStorage.removeItem('token');
          return of(null);
        })
      ).subscribe(user => {
        if (user) {
          this.currentUserSubject.next(user);
        }
      });
    }
  }

  login(credentials: UserLogin): Observable<Token> {
    // Converter para o formato esperado pela API (OAuth2PasswordRequestForm)
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    return this.http.post<Token>(`${this.apiUrl}/login`, formData).pipe(
      tap(response => {
        localStorage.setItem('token', response.access_token);
        this.getProfile().subscribe(user => {
          this.currentUserSubject.next(user);
        });
      })
    );
  }

  register(userData: UserRegister): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/register`, userData);
  }

  getProfile(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/me`);
  }

  logout(): void {
    localStorage.removeItem('token');
    this.currentUserSubject.next(null);
    this.router.navigate(['/login']);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}