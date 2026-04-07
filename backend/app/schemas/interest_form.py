from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InterestFormBase(BaseModel):
    full_name: str
    phone: str

class InterestFormCreate(InterestFormBase):
    pass

class InterestFormResponse(InterestFormBase):
    id: str
    user_id: str
    pet_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class InterestFormResponseWithDetails(InterestFormResponse):
    pet_name: Optional[str] = None
    organization_name: Optional[str] = None
