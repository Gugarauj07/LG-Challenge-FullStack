import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiConfigService {
  private apiBaseUrl: string;

  constructor() {
    // Sempre usar a URL do environment, que agora está definida corretamente em environment.prod.ts
    this.apiBaseUrl = environment.apiUrl;
    console.log('Usando API URL:', this.apiBaseUrl);
  }

  getApiUrl(): string {
    return this.apiBaseUrl;
  }
}