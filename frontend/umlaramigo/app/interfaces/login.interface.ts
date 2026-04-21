export interface UserBase {
  email: string;
  full_name: string;
}

export interface UserCreate extends UserBase {
  password: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface AuthState {
  user: UserResponse | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
}

export interface UserResponse {
  email: string;
  full_name: string;
  id: string;
  created_at: string;
  is_active: boolean;
}

export interface ResponseLoginDto {
  user: UserResponse;
  access_token: string;
  token_type: string;
}
