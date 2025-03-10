import { Component, Input } from '@angular/core';
import { Movie } from '../../models/movie.model';
import { FavoritesService } from '../../services/favorites.service';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-movie-card',
  templateUrl: './movie-card.component.html',
  styleUrls: ['./movie-card.component.scss']
})
export class MovieCardComponent {
  @Input() movie!: Movie;

  constructor(
    private favoritesService: FavoritesService,
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  isFavorite(movieId: number): boolean {
    return this.favoritesService.isFavorite(movieId);
  }

  toggleFavorite(movieId: number): void {
    if (!this.authService.isAuthenticated()) {
      this.snackBar.open('Você precisa estar logado para adicionar favoritos', 'Entendi', {
        duration: 3000
      });
      this.router.navigate(['/login']);
      return;
    }

    if (this.isFavorite(movieId)) {
      this.favoritesService.removeFromFavorites(movieId).subscribe({
        next: () => {
          this.snackBar.open('Filme removido dos favoritos', 'Fechar', {
            duration: 2000
          });
        },
        error: (err) => {
          console.error('Erro ao remover dos favoritos:', err);
          this.snackBar.open('Erro ao remover dos favoritos', 'Fechar', {
            duration: 2000
          });
        }
      });
    } else {
      this.favoritesService.addToFavorites(movieId).subscribe({
        next: () => {
          this.snackBar.open('Filme adicionado aos favoritos', 'Fechar', {
            duration: 2000
          });
        },
        error: (err) => {
          console.error('Erro ao adicionar aos favoritos:', err);
          this.snackBar.open('Erro ao adicionar aos favoritos', 'Fechar', {
            duration: 2000
          });
        }
      });
    }
  }
}