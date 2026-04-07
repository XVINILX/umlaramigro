import type { InterestFormResponse } from "./interest-form.interface";

export enum PetType {
  DOG = "dog",
  CAT = "cat",
}

export interface PetBase {
  name: string;
  pet_type: PetType;
  description?: string;
}

export interface PetCreate extends PetBase {}

export interface PetUpdate {
  name?: string;
  description?: string;
}

export interface PetResponse extends PetBase {
  id: string;
  organization_id: string;
  created_at: string; // ISO datetime string
}

export interface PetResponseWithInterests extends PetResponse {
  interest_forms?: InterestFormResponse[];
}
