from abc import ABC, abstractmethod
from typing import Optional, List
from app.models import Organization
from app.schemas import OrganizationCreate, OrganizationUpdate


class IOrganizationRepository(ABC):
    """Interface para repositório de organizações."""

    @abstractmethod
    async def create(self, org: OrganizationCreate, owner_id: int) -> Organization:
        """Criar uma nova organização."""
        pass

    @abstractmethod
    async def get_by_id(self, org_id: int) -> Optional[Organization]:
        """Obter organização por ID."""
        pass

    @abstractmethod
    async def get_by_owner(self, owner_id: int) -> List[Organization]:
        """Obter organizações de um proprietário."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Organization]:
        """Listar todas as organizações."""
        pass

    @abstractmethod
    async def update(self, org_id: int, org_update: OrganizationUpdate) -> Optional[Organization]:
        """Atualizar organização."""
        pass

    @abstractmethod
    async def delete(self, org_id: int) -> bool:
        """Deletar organização."""
        pass

