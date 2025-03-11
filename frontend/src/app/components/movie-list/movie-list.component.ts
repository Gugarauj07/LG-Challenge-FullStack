import { Component, OnInit } from '@angular/core';
import { MovieService } from '../../services/movie.service';
import { Movie } from '../../models/movie.model';
import { PageEvent } from '@angular/material/paginator';

@Component({
  selector: 'app-movie-list',
  templateUrl: './movie-list.component.html',
  styleUrls: ['./movie-list.component.scss']
})
export class MovieListComponent implements OnInit {
  movies: Movie[] = [];
  loading = true;
  error = false;

  // Paginação
  pageSize = 12;
  pageSizeOptions = [6, 12, 24, 48];
  totalMovies = 0;
  currentPage = 0;

  constructor(private movieService: MovieService) { }

  ngOnInit(): void {
    this.loadMovies();
  }

  loadMovies(): void {
    this.loading = true;

    const skip = this.currentPage * this.pageSize;

    this.movieService.getTopRated(skip, this.pageSize).subscribe({
      next: (response) => {
        this.movies = response.items;
        this.totalMovies = response.total;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erro ao carregar filmes:', err);
        this.error = true;
        this.loading = false;
      }
    });
  }

  handlePageEvent(event: PageEvent): void {
    this.currentPage = event.pageIndex;
    this.pageSize = event.pageSize;
    this.loadMovies();
  }
}