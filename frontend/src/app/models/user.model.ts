export interface User {
  id: number;
  username: string;
  email?: string;
  is_active: boolean;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface UserRegister {
  username: string;
  email?: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}