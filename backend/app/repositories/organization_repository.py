from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy.orm import Session
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


class OrganizationRepository(IOrganizationRepository):
    """Implementação SQLAlchemy do repositório de organizações."""

    def __init__(self, db: Session):
        self.db = db

    async def create(self, org: OrganizationCreate, owner_id: int) -> Organization:
        """Criar uma nova organização."""
        db_org = Organization(
            name=org.name,
            description=org.description,
            owner_id=owner_id,
        )
        self.db.add(db_org)
        self.db.flush()
        return db_org

    async def get_by_id(self, org_id: int) -> Optional[Organization]:
        """Obter organização por ID."""
        return self.db.query(Organization).filter(Organization.id == org_id).first()

    async def get_by_owner(self, owner_id: int) -> List[Organization]:
        """Obter organizações de um proprietário."""
        return self.db.query(Organization).filter(Organization.owner_id == owner_id).all()

    async def list_all(self) -> List[Organization]:
        """Listar todas as organizações."""
        return self.db.query(Organization).all()

    async def update(self, org_id: int, org_update: OrganizationUpdate) -> Optional[Organization]:
        """Atualizar organização."""
        org = await self.get_by_id(org_id)
        if not org:
            return None

        if org_update.name:
            org.name = org_update.name
        if org_update.description:
            org.description = org_update.description

        self.db.flush()
        return org

    async def delete(self, org_id: int) -> bool:
        """Deletar organização."""
        org = await self.get_by_id(org_id)
        if not org:
            return False
        self.db.delete(org)
        self.db.flush()
        return True
