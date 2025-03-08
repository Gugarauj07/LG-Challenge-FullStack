import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../services/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {
  registerForm: FormGroup;
  loading = false;
  hidePassword = true;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    this.registerForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  onSubmit(): void {
    if (this.registerForm.invalid) {
      return;
    }

    this.loading = true;

    this.authService.register(this.registerForm.value).subscribe({
      next: () => {
        this.snackBar.open('Cadastro realizado com sucesso! Faça login para continuar.', 'Fechar', {
          duration: 5000
        });
        this.router.navigate(['/login']);
      },
      error: (error) => {
        let errorMessage = 'Erro ao realizar cadastro.';

        if (error.error && error.error.detail) {
          errorMessage = error.error.detail;
        }

        this.snackBar.open(errorMessage, 'Fechar', {
          duration: 5000,
          panelClass: ['error-snackbar']
        });

        this.loading = false;
      }
    });
  }
}