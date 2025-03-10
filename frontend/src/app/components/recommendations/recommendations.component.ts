import { Component, OnInit } from '@angular/core';
import { RecommendationService } from '../../services/recommendation.service';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { Movie } from '../../models/movie.model';

@Component({
  selector: 'app-recommendations',
  templateUrl: './recommendations.component.html',
  styleUrls: ['./recommendations.component.scss']
})
export class RecommendationsComponent implements OnInit {
  recommendations: Movie[] = [];
  loading = true;
  error = false;

  constructor(
    private recommendationService: RecommendationService,
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit(): void {
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }
    this.loadRecommendations();
  }

  loadRecommendations(): void {
    this.loading = true;
    this.recommendationService.getUserRecommendations(12).subscribe({
      next: (movies) => {
        this.recommendations = movies;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erro ao carregar recomendações:', err);
        this.error = true;
        this.loading = false;
      }
    });
  }
}