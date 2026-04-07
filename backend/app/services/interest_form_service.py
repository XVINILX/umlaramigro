from app.schemas import InterestFormCreate
from app.repositories import IInterestFormRepository


class InterestFormService:
    def __init__(self, form_repo: IInterestFormRepository):
        self.form_repo = form_repo

    async def create_interest_form(self, form: InterestFormCreate, user_id: int, pet_id: int):
        return await self.form_repo.create(form, user_id, pet_id)

    async def get_interest_form_by_id(self, form_id: int):
        return await self.form_repo.get_by_id(form_id)

    async def get_interest_forms_by_pet(self, pet_id: int) -> list:
        return await self.form_repo.get_by_pet(pet_id)

    async def get_interest_forms_by_user(self, user_id: int) -> list:
        return await self.form_repo.get_by_user(user_id)

    async def list_interest_forms(self) -> list:
        return await self.form_repo.list_all()

    async def delete_interest_form(self, form_id: int) -> bool:
        return await self.form_repo.delete(form_id)

    async def get_interest_forms_with_details(self, pet_id: int) -> list:
        return await self.form_repo.get_with_details(pet_id)
