from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: str
    owner_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class OrganizationResponseWithPets(OrganizationResponse):
    pets: List = []
