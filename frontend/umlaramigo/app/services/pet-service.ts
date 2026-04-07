import axios from "axios";
import apiClient from "./api-client";
import type {
  PetResponse,
  PetResponseWithInterests,
  PetCreate,
  PetUpdate,
} from "../interfaces/pet.interface";

class PetService {
  /**
   * Get all pets available for adoption
   */
  async getAllPets(): Promise<PetResponse[]> {
    try {
      const response = await apiClient.get<PetResponse[]>("/pets");
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Get all pets from a specific organization
   */
  async getPetsByOrganization(orgId: string | number): Promise<PetResponse[]> {
    try {
      const response = await apiClient.get<PetResponse[]>(
        `/pets/organization/${orgId}`,
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Get a specific pet by ID with interest forms
   */
  async getPetById(petId: string | number): Promise<PetResponseWithInterests> {
    try {
      const response = await apiClient.get<PetResponseWithInterests>(
        `/pets/${petId}`,
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Create a new pet (requires authentication)
   */
  async createPet(
    pet: PetCreate,
    orgId: string | number,
  ): Promise<PetResponse> {
    try {
      const response = await apiClient.post<PetResponse>("/pets", pet, {
        params: { org_id: orgId },
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Update pet information (requires authentication)
   */
  async updatePet(
    petId: string | number,
    petUpdate: PetUpdate,
  ): Promise<PetResponse> {
    try {
      const response = await apiClient.put<PetResponse>(
        `/pets/${petId}`,
        petUpdate,
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Delete a pet (requires authentication)
   */
  async deletePet(petId: string | number): Promise<{ message: string }> {
    try {
      const response = await apiClient.delete<{ message: string }>(
        `/pets/${petId}`,
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

export default new PetService();
