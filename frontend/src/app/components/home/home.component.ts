import { Component, OnInit } from '@angular/core';
import { MovieService } from '../../services/movie.service';
import { Movie, MovieStats } from '../../models/movie.model';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  topMovies: Movie[] = [];
  movieStats: MovieStats | null = null;
  loading = true;
  error = false;

  constructor(private movieService: MovieService) { }

  ngOnInit(): void {
    this.loadTopMovies();
    this.loadMovieStats();
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

  loadMovieStats(): void {
    this.movieService.getMovieStats().subscribe({
      next: (stats) => {
        this.movieStats = stats;
      },
      error: (err) => {
        console.error('Erro ao carregar estatísticas:', err);
      }
    });
  }
}