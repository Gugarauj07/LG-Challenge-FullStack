import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { RecommendationService } from '../../services/recommendation.service';
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
    private movieService: MovieService,
    private recommendationService: RecommendationService
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
}