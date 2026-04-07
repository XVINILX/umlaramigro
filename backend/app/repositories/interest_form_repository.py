from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from app.models import InterestForm, Pet, Organization
from app.schemas import InterestFormCreate


class IInterestFormRepository(ABC):
    """Interface para repositório de formulários de interesse."""

    @abstractmethod
    async def create(self, form: InterestFormCreate, user_id: int, pet_id: int) -> InterestForm:
        """Criar um novo formulário de interesse."""
        pass

    @abstractmethod
    async def get_by_id(self, form_id: int) -> Optional[InterestForm]:
        """Obter formulário por ID."""
        pass

    @abstractmethod
    async def get_by_pet(self, pet_id: int) -> List[InterestForm]:
        """Obter formulários de um pet."""
        pass

    @abstractmethod
    async def get_by_user(self, user_id: int) -> List[InterestForm]:
        """Obter formulários de um usuário."""
        pass

    @abstractmethod
    async def list_all(self) -> List[InterestForm]:
        """Listar todos os formulários."""
        pass

    @abstractmethod
    async def delete(self, form_id: int) -> bool:
        """Deletar formulário."""
        pass

    @abstractmethod
    async def get_with_details(self, pet_id: int) -> List[Tuple]:
        """Obter formulários com detalhes de pet e organização."""
        pass


class InterestFormRepository(IInterestFormRepository):
    """Implementação SQLAlchemy do repositório de formulários de interesse."""

    def __init__(self, db: Session):
        self.db = db

    async def create(self, form: InterestFormCreate, user_id: int, pet_id: int) -> InterestForm:
        """Criar um novo formulário de interesse."""
        db_form = InterestForm(
            full_name=form.full_name,
            phone=form.phone,
            user_id=user_id,
            pet_id=pet_id,
        )
        self.db.add(db_form)
        self.db.flush()
        return db_form

    async def get_by_id(self, form_id: int) -> Optional[InterestForm]:
        """Obter formulário por ID."""
        return self.db.query(InterestForm).filter(InterestForm.id == form_id).first()

    async def get_by_pet(self, pet_id: int) -> List[InterestForm]:
        """Obter formulários de um pet."""
        return self.db.query(InterestForm).filter(InterestForm.pet_id == pet_id).all()

    async def get_by_user(self, user_id: int) -> List[InterestForm]:
        """Obter formulários de um usuário."""
        return self.db.query(InterestForm).filter(InterestForm.user_id == user_id).all()

    async def list_all(self) -> List[InterestForm]:
        """Listar todos os formulários."""
        return self.db.query(InterestForm).all()

    async def delete(self, form_id: int) -> bool:
        """Deletar formulário."""
        form = await self.get_by_id(form_id)
        if not form:
            return False
        self.db.delete(form)
        self.db.flush()
        return True

    async def get_with_details(self, pet_id: int) -> List[Tuple]:
        """Obter formulários com detalhes de pet e organização."""
        return (
            self.db.query(InterestForm, Pet.name, Organization.name)
            .join(Pet)
            .join(Organization)
            .filter(InterestForm.pet_id == pet_id)
            .all()
        )
