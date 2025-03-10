import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
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
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.searchForm = this.fb.group({
      title: [''],
      year: [''],
      genres: [[]]
    });
  }

  ngOnInit(): void {
    // Verificar se há parâmetros de busca na URL
    this.route.queryParams.subscribe(params => {
      const title = params['title'] || '';
      const year = params['year'] || '';
      let genres: string[] = [];

      // Verifica se o parâmetro genre existe (compatibilidade com versão antiga)
      if (params['genre']) {
        genres.push(params['genre']);
      }

      // Verifica se há múltiplos gêneros na URL
      if (params['genres']) {
        if (Array.isArray(params['genres'])) {
          genres = genres.concat(params['genres']);
        } else {
          genres.push(params['genres']);
        }
      }

      if (title || year || genres.length > 0) {
        this.searchForm.patchValue({
          title: title,
          year: year,
          genres: genres
        });

        // Se tiver parâmetros de ano ou gênero, mostra automaticamente os filtros
        if (year || genres.length > 0) {
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
    if (!formValue.title && !formValue.year && (!formValue.genres || formValue.genres.length === 0)) {
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

    if (formValue.genres && formValue.genres.length > 0) {
      query.genres = formValue.genres;
    }

    // Atualizar URL com os parâmetros de busca
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        title: formValue.title || null,
        year: formValue.year || null,
        genres: formValue.genres && formValue.genres.length > 0 ? formValue.genres : null
      },
      queryParamsHandling: 'merge'
    });

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
    this.searchForm.reset({
      title: '',
      year: '',
      genres: []
    });
    this.movies = [];
    this.searched = false;
    this.showFilters = false;

    // Limpar parâmetros da URL
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {}
    });
  }
}