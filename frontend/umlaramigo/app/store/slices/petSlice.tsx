// store/slices/petsSlice.ts
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import apiClient from "~/services/api-client";
import type {
  PetCreate,
  PetResponse,
  PetUpdate,
} from "~/interfaces/pet.interface";

interface PresignedUrlResponse {
  upload_url: string;
  image_url: string;
}

interface PetsState {
  pets: PetResponse[];
  isLoading: boolean;
  error: string | null;
  successMessage: string | null;
}

const initialState: PetsState = {
  pets: [],
  isLoading: false,
  error: null,
  successMessage: null,
};

// Buscar pets da organização
export const fetchOrganizationPets = createAsyncThunk(
  "pets/fetchOrganizationPets",
  async (organizationId: string) => {
    const response = await apiClient.get<PetResponse[]>(
      `/organizations/${organizationId}/pets`,
    );
    return response.data;
  },
);

// Criar novo pet
export const createPet = createAsyncThunk(
  "pets/createPet",
  async (petData: PetCreate) => {
    const response = await apiClient.post<PetResponse>("/pets", petData);
    return response.data;
  },
);

export const updatePet = createAsyncThunk(
  "pets/updatePet",
  async ({ id, data }: { id: string; data: PetUpdate }) => {
    const response = await apiClient.put<PetResponse>(`/pets/${id}`, data);
    return response.data;
  },
);

// Deletar pet
export const deletePet = createAsyncThunk(
  "pets/deletePet",
  async (id: string) => {
    await apiClient.delete(`/pets/${id}`);
    return id;
  },
);

// Upload de imagem do pet
export const uploadPetImage = createAsyncThunk(
  "pets/uploadPetImage",
  async ({ petId, file }: { petId: string; file: File }) => {
    const fileType = file.type;
    const fileName = file.name;

    const presignedResponse = await apiClient.get<PresignedUrlResponse>(
      `/pets/${petId}/upload-url`,
      {
        params: { file_type: fileType, file_name: fileName },
      },
    );

    const { upload_url, image_url } = presignedResponse.data;

    await fetch(upload_url, {
      method: "PUT",
      body: file,
      headers: {
        "Content-Type": fileType,
      },
    });

    return image_url;
  },
);

const petsSlice = createSlice({
  name: "pets",
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearSuccess: (state) => {
      state.successMessage = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch pets
      .addCase(fetchOrganizationPets.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchOrganizationPets.fulfilled, (state, action) => {
        state.isLoading = false;
        state.pets = action.payload;
      })
      .addCase(fetchOrganizationPets.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || "Erro ao buscar pets";
      })
      // Create pet
      .addCase(createPet.pending, (state) => {
        state.isLoading = true;
        state.error = null;
        state.successMessage = null;
      })
      .addCase(createPet.fulfilled, (state, action) => {
        state.isLoading = false;
        state.pets.push(action.payload);
        state.successMessage = "Pet cadastrado com sucesso!";
      })
      .addCase(createPet.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || "Erro ao cadastrar pet";
      })
      // Update pet
      .addCase(updatePet.fulfilled, (state, action) => {
        const index = state.pets.findIndex(
          (pet) => pet.id === action.payload.id,
        );
        if (index !== -1) {
          state.pets[index] = action.payload;
        }
        state.successMessage = "Pet atualizado com sucesso!";
      })
      // Delete pet
      .addCase(deletePet.fulfilled, (state, action) => {
        state.pets = state.pets.filter((pet) => pet.id !== action.payload);
        state.successMessage = "Pet removido com sucesso!";
      })
      // Upload pet image
      .addCase(uploadPetImage.fulfilled, (state, action) => {
        state.successMessage = "Imagem do pet enviada com sucesso!";
      });
  },
});

export const { clearError, clearSuccess } = petsSlice.actions;
export default petsSlice.reducer;
