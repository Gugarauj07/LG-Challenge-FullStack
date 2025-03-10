import { Component, OnInit } from '@angular/core';
import { FavoritesService } from '../../services/favorites.service';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { Movie } from '../../models/movie.model';

@Component({
  selector: 'app-favorites',
  templateUrl: './favorites.component.html',
  styleUrls: ['./favorites.component.scss']
})
export class FavoritesComponent implements OnInit {
  favorites: Movie[] = [];
  loading = true;
  error = false;

  constructor(
    private favoritesService: FavoritesService,
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit(): void {
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }
    this.loadFavorites();
  }

  loadFavorites(): void {
    this.loading = true;
    this.favoritesService.getFavorites().subscribe({
      next: (movies) => {
        this.favorites = movies;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erro ao carregar favoritos:', err);
        this.error = true;
        this.loading = false;
      }
    });
  }
}