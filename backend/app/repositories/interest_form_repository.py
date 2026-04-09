from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from app.models import InterestForm
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

