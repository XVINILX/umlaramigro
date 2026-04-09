from abc import ABC, abstractmethod
from typing import Optional, List
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

