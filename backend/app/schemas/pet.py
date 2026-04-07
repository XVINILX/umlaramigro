from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

from app.schemas.interest_form import InterestFormResponse

class PetType(str, Enum):
    DOG = "dog"
    CAT = "cat"

class PetBase(BaseModel):
    name: str
    pet_type: PetType
    description: Optional[str] = None

class PetCreate(PetBase):
    pass

class PetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class PetResponse(PetBase):
    id: str
    organization_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class PetResponseWithInterests(PetResponse):
    interest_forms: List[InterestFormResponse] = []

