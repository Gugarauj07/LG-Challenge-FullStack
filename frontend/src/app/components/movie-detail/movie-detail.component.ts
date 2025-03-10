import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { RecommendationService } from '../../services/recommendation.service';
import { FavoritesService } from '../../services/favorites.service';
import { AuthService } from '../../services/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Movie } from '../../models/movie.model';

@Component({
  selector: 'app-movie-detail',
  templateUrl: './movie-detail.component.html',
  styleUrls: ['./movie-detail.component.scss']
})
export class MovieDetailComponent implements OnInit {
  movie: Movie | null = null;
  similarMovies: Movie[] = [];
  loading = true;
  error = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private movieService: MovieService,
    private recommendationService: RecommendationService,
    private favoritesService: FavoritesService,
    private authService: AuthService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const movieId = +params['id'];
      this.loadMovie(movieId);
      this.loadSimilarMovies(movieId);
    });
  }

  loadMovie(id: number): void {
    this.loading = true;
    this.movieService.getMovieById(id).subscribe({
      next: (movie) => {
        this.movie = movie;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erro ao carregar detalhes do filme:', err);
        this.error = true;
        this.loading = false;
      }
    });
  }

  loadSimilarMovies(id: number): void {
    this.recommendationService.getSimilarMovies(id, 4).subscribe({
      next: (movies) => {
        this.similarMovies = movies;
      },
      error: (err) => {
        console.error('Erro ao carregar filmes similares:', err);
      }
    });
  }

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