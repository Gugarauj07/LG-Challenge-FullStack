import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private router: Router) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    // Recupera o token do localStorage
    const token = localStorage.getItem('token');

    // Se o token existir, adiciona ao cabeçalho da requisição
    if (token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        // Só redireciona para o login em caso de erro 401 se for uma requisição específica
        // como a de perfil do usuário, para evitar redirecionamentos indesejados
        if (error.status === 401) {
          // Verifica se a requisição é para o endpoint de perfil do usuário
          const isProfileRequest = request.url.includes('/auth/me');

          // Remove o token apenas se for uma requisição de perfil (evita redirecionamentos indesejados)
          localStorage.removeItem('token');

          // Só redireciona para o login se estiver tentando acessar o perfil
          if (isProfileRequest && !this.router.url.includes('/login')) {
            this.router.navigate(['/login']);
          }
        }
        return throwError(() => error);
      })
    );
  }
}