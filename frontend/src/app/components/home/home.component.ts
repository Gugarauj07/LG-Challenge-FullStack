import { Component, OnInit } from '@angular/core';
import { MovieService } from '../../services/movie.service';
import { RecommendationService } from '../../services/recommendation.service';
import { AuthService } from '../../services/auth.service';
import { FavoritesService } from '../../services/favorites.service';
import { Movie, MovieStats } from '../../models/movie.model';
import { catchError, of } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  topMovies: Movie[] = [];
  recommendedMovies: Movie[] = [];
  movieStats: MovieStats | null = null;
  loading = true;
  loadingRecommendations = false;
  loadingStats = true;
  error = false;
  recommendationsError = false;
  statsError = false;
  isLoggedIn = false;

  constructor(
    private movieService: MovieService,
    private recommendationService: RecommendationService,
    private authService: AuthService,
    private favoritesService: FavoritesService
  ) { }

  ngOnInit(): void {
    this.loadTopMovies();
    this.loadMovieStatsSafely();

    // Verifica se o usuário está autenticado
    this.isLoggedIn = this.authService.isAuthenticated();

    // Se o usuário estiver logado, carrega os dados que precisam de autenticação
    if (this.isLoggedIn) {
      this.loadRecommendationsSafely();
      this.loadFavoritesSafely();
    }
  }

  loadTopMovies(): void {
    this.movieService.getTopRated(6).subscribe({
      next: (movies) => {
        this.topMovies = movies;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erro ao carregar filmes:', err);
        this.error = true;
        this.loading = false;
      }
    });
  }

  loadMovieStatsSafely(): void {
    this.loadingStats = true;

    this.movieService.getMovieStats()
      .pipe(
        catchError(err => {
          console.error('Erro ao carregar estatísticas:', err);
          this.statsError = true;
          this.loadingStats = false;
          return of(null);
        })
      )
      .subscribe(stats => {
        if (stats) {
          this.movieStats = stats;
        }
        this.loadingStats = false;
      });
  }

  loadRecommendationsSafely(): void {
    this.loadingRecommendations = true;

    this.recommendationService.getUserRecommendations(6)
      .pipe(
        catchError(err => {
          console.error('Erro ao carregar recomendações:', err);
          this.recommendationsError = true;
          this.loadingRecommendations = false;
          return of([]);
        })
      )
      .subscribe(movies => {
        this.recommendedMovies = movies;
        this.loadingRecommendations = false;
      });
  }

  loadFavoritesSafely(): void {
    // Carrega os favoritos de maneira segura
    this.favoritesService.getFavorites()
      .pipe(
        catchError(err => {
          console.error('Erro ao carregar favoritos:', err);
          return of([]);
        })
      )
      .subscribe(() => {
        // Os favoritos já são carregados no serviço
        // Não é necessário fazer mais nada aqui, pois o BehaviorSubject no serviço já foi atualizado
      });
  }
}