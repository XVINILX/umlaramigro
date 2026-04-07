from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import Pet
from app.schemas import PetCreate, PetUpdate


class IPetRepository(ABC):
    """Interface para repositório de pets."""

    @abstractmethod
    async def create(self, pet: PetCreate, organization_id: int) -> Pet:
        """Criar um novo pet."""
        pass

    @abstractmethod
    async def get_by_id(self, pet_id: int) -> Optional[Pet]:
        """Obter pet por ID."""
        pass

    @abstractmethod
    async def get_by_organization(self, organization_id: int) -> List[Pet]:
        """Obter pets de uma organização."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Pet]:
        """Listar todos os pets."""
        pass

    @abstractmethod
    async def update(self, pet_id: int, pet_update: PetUpdate) -> Optional[Pet]:
        """Atualizar pet."""
        pass

    @abstractmethod
    async def delete(self, pet_id: int) -> bool:
        """Deletar pet."""
        pass


class PetRepository(IPetRepository):
    """Implementação SQLAlchemy do repositório de pets."""

    def __init__(self, db: Session):
        self.db = db

    async def create(self, pet: PetCreate, organization_id: int) -> Pet:
        """Criar um novo pet."""
        db_pet = Pet(
            name=pet.name,
            pet_type=pet.pet_type,
            description=pet.description,
            organization_id=organization_id,
        )
        self.db.add(db_pet)
        self.db.flush()
        return db_pet

    async def get_by_id(self, pet_id: int) -> Optional[Pet]:
        """Obter pet por ID."""
        return self.db.query(Pet).filter(Pet.id == pet_id).first()

    async def get_by_organization(self, organization_id: int) -> List[Pet]:
        """Obter pets de uma organização."""
        return self.db.query(Pet).filter(Pet.organization_id == organization_id).all()

    async def list_all(self) -> List[Pet]:
        """Listar todos os pets."""
        return self.db.query(Pet).all()

    async def update(self, pet_id: int, pet_update: PetUpdate) -> Optional[Pet]:
        """Atualizar pet."""
        pet = await self.get_by_id(pet_id)
        if not pet:
            return None

        if pet_update.name:
            pet.name = pet_update.name
        if pet_update.description:
            pet.description = pet_update.description

        self.db.flush()
        return pet

    async def delete(self, pet_id: int) -> bool:
        """Deletar pet."""
        pet = await self.get_by_id(pet_id)
        if not pet:
            return False
        self.db.delete(pet)
        self.db.flush()
        return True
