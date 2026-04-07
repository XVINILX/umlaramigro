from app.schemas import OrganizationCreate, OrganizationUpdate
from app.repositories import IOrganizationRepository


class OrganizationService:
    def __init__(self, org_repo: IOrganizationRepository):
        self.org_repo = org_repo

    async def create_organization(self, org: OrganizationCreate, owner_id: int):
        return await self.org_repo.create(org, owner_id)

    async def get_organization_by_id(self, org_id: int):
        return await self.org_repo.get_by_id(org_id)

    async def get_organizations_by_owner(self, owner_id: int) -> list:
        return await self.org_repo.get_by_owner(owner_id)

    async def update_organization(self, org_id: int, org_update: OrganizationUpdate):
        return await self.org_repo.update(org_id, org_update)

    async def list_organizations(self) -> list:
        return await self.org_repo.list_all()

    async def delete_organization(self, org_id: int) -> bool:
        return await self.org_repo.delete(org_id)
