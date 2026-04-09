from abc import ABC, abstractmethod
from typing import Optional, List
from app.models import User
from app.schemas import UserCreate, UserUpdate


class IUserRepository(ABC):
    """Interface para repositório de usuários."""

    @abstractmethod
    async def create(self, user: UserCreate) -> User:
        """Criar um novo usuário."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Obter usuário por ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Obter usuário por email."""
        pass

    @abstractmethod
    async def list_all(self) -> List[User]:
        """Listar todos os usuários."""
        pass

    @abstractmethod
    async def update(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Atualizar usuário."""
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """Deletar usuário."""
        pass

