import axios from "axios";
import type {
  ResponseLoginDto,
  UserCreate,
  UserLogin,
  UserResponse,
} from "~/interfaces/login.interface";
import apiClient from "./api-client";

class AuthService {
  public async register(data: UserCreate) {
    try {
      const response = await apiClient.post<UserResponse>(
        "/auth/register",
        data,
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  public async login(data: UserLogin) {
    try {
      const response = await apiClient.post<ResponseLoginDto>(
        "/auth/login",
        data,
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Handle API errors
   */
  private handleError(error: unknown): Error {
    if (axios.isAxiosError(error)) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "An error occurred while processing your request";
      return new Error(message);
    }
    return error instanceof Error ? error : new Error("Unknown error occurred");
  }
}

export default new AuthService();
