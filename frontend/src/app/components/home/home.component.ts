import { Component, OnInit, AfterViewInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Chart, registerables } from 'chart.js';

import { MovieService } from '../../services/movie.service';
import { Movie, MovieStats } from '../../models/movie.model';

// Registra todos os componentes do Chart.js
Chart.register(...registerables);

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, AfterViewInit {
  topMovies$: Observable<Movie[]>;
  movieStats$: Observable<MovieStats>;
  genresChart: any;

  constructor(private movieService: MovieService) {
    this.topMovies$ = this.movieService.getTopRatedMovies(6);
    this.movieStats$ = this.movieService.getMovieStats();
  }

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
    // Atraso para garantir que os dados já foram carregados
    setTimeout(() => {
      this.createGenresChart();
    }, 1000);
  }

  getMovieImage(movie: Movie): string {
    const image = this.movieService.getTMDBImageUrl(movie);
    return image || 'assets/images/movie-placeholder.jpg';
  }

  private createGenresChart(): void {
    this.movieStats$.subscribe(stats => {
      if (!stats || !stats.top_genres || stats.top_genres.length === 0) {
        return;
      }

      const canvas = document.getElementById('genresChart') as HTMLCanvasElement;
      if (!canvas) {
        return;
      }

      const labels = stats.top_genres.map(genre => genre.name);
      const data = stats.top_genres.map(genre => genre.movie_count);

      this.genresChart = new Chart(canvas, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Número de Filmes',
            data: data,
            backgroundColor: [
              'rgba(63, 81, 181, 0.7)',  // Indigo
              'rgba(33, 150, 243, 0.7)', // Blue
              'rgba(0, 188, 212, 0.7)',  // Cyan
              'rgba(0, 150, 136, 0.7)',  // Teal
              'rgba(76, 175, 80, 0.7)',  // Green
              'rgba(139, 195, 74, 0.7)', // Light Green
              'rgba(205, 220, 57, 0.7)', // Lime
              'rgba(255, 235, 59, 0.7)', // Yellow
              'rgba(255, 193, 7, 0.7)',  // Amber
              'rgba(255, 152, 0, 0.7)'   // Orange
            ],
            borderColor: [
              'rgba(63, 81, 181, 1)',
              'rgba(33, 150, 243, 1)',
              'rgba(0, 188, 212, 1)',
              'rgba(0, 150, 136, 1)',
              'rgba(76, 175, 80, 1)',
              'rgba(139, 195, 74, 1)',
              'rgba(205, 220, 57, 1)',
              'rgba(255, 235, 59, 1)',
              'rgba(255, 193, 7, 1)',
              'rgba(255, 152, 0, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    });
  }
}
