import { Injectable } from '@angular/core';
import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  UrlTree,
  Router
} from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    // Verificar se o usuário está autenticado
    const token = localStorage.getItem('token');

    if (token) {
      return true;
    }

    // Redirecionar para a página de login se não estiver autenticado
    this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
    return false;
  }
}