from app.schemas import PetCreate, PetUpdate
from app.repositories import IPetRepository


class PetService:
    def __init__(self, pet_repo: IPetRepository):
        self.pet_repo = pet_repo

    async def create_pet(self, pet: PetCreate, organization_id: int):
        return await self.pet_repo.create(pet, organization_id)

    async def get_pet_by_id(self, pet_id: int):
        return await self.pet_repo.get_by_id(pet_id)

    async def get_pets_by_organization(self, organization_id: int) -> list:
        return await self.pet_repo.get_by_organization(organization_id)

    async def update_pet(self, pet_id: int, pet_update: PetUpdate):
        return await self.pet_repo.update(pet_id, pet_update)

    async def list_pets(self) -> list:
        return await self.pet_repo.list_all()

    async def delete_pet(self, pet_id: int) -> bool:
        return await self.pet_repo.delete(pet_id)
        self.db.flush()
        return True
