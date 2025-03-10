import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { Movie } from '../../models/movie.model';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  searchForm: FormGroup;
  movies: Movie[] = [];
  loading = false;
  searched = false;
  showFilters = false;
  availableGenres: string[] = [
    'Action', 'Adventure', 'Animation', 'Children', 'Comedy',
    'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
    'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance',
    'Sci-Fi', 'Thriller', 'War', 'Western'
  ];

  constructor(
    private fb: FormBuilder,
    private movieService: MovieService,
    private route: ActivatedRoute
  ) {
    this.searchForm = this.fb.group({
      title: [''],
      year: [''],
      genre: ['']
    });
  }

  ngOnInit(): void {
    // Verificar se há parâmetros de busca na URL
    this.route.queryParams.subscribe(params => {
      if (params['title'] || params['year'] || params['genre']) {
        this.searchForm.patchValue({
          title: params['title'] || '',
          year: params['year'] || '',
          genre: params['genre'] || ''
        });

        // Se tiver parâmetros de ano ou gênero, mostra automaticamente os filtros
        if (params['year'] || params['genre']) {
          this.showFilters = true;
        }

        this.search();
      }
    });
  }

  toggleFilters(): void {
    this.showFilters = !this.showFilters;
  }

  search(): void {
    // Não realizar busca se todos os campos estiverem vazios
    const formValue = this.searchForm.value;
    if (!formValue.title && !formValue.year && !formValue.genre) {
      return;
    }

    this.loading = true;
    this.searched = true;

    const query: any = {};

    if (formValue.title) {
      query.title = formValue.title.trim();
    }

    if (formValue.year) {
      query.year = parseInt(formValue.year, 10);
    }

    if (formValue.genre) {
      query.genre = formValue.genre;
    }

    this.movieService.searchMovies(query).subscribe({
      next: (movies) => {
        this.movies = movies;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erro ao buscar filmes:', err);
        this.loading = false;
        this.movies = [];
      }
    });
  }

  clearSearch(): void {
    this.searchForm.reset();
    this.movies = [];
    this.searched = false;
    this.showFilters = false;
  }
}