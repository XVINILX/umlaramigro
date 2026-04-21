import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import type {
  ResponseLoginDto,
  UserCreate,
} from "~/interfaces/login.interface";
import authService from "~/services/auth.service";
// Interfaces baseadas nos modelos Python
interface UserBase {
  email: string;
  full_name: string;
}

interface UserLogin {
  email: string;
  password: string;
}

interface AuthState {
  user: UserBase | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  token: null,
  isLoading: false,
  error: null,
};

export const login = createAsyncThunk(
  "auth/login",
  async (credentials: UserLogin) => {
    const response = await authService.login(credentials);

    localStorage.setItem("token", response.access_token);

    return { user: response.user, token: response.access_token };
  },
);

export const register = createAsyncThunk(
  "auth/register",
  async (userData: UserCreate) => {
    const response = await authService.register(userData);

    return response;
  },
);

export const logout = createAsyncThunk("auth/logout", async () => {
  localStorage.removeItem("token");
  return null;
});

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload.user;
        state.token = action.payload.token;
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || "Email ou senha inválidos";
      })
      .addCase(logout.fulfilled, (state) => {
        state.user = null;
        state.token = null;
      });
  },
});

export const { clearError } = authSlice.actions;
export default authSlice.reducer;
