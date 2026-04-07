from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy.orm import Session
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


class UserRepository(IUserRepository):
    """Implementação SQLAlchemy do repositório de usuários."""

    def __init__(self, db: Session):
        self.db = db

    async def create(self, user: UserCreate) -> User:
        """Criar um novo usuário."""
        from app.core import get_password_hash
        
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
        )
        self.db.add(db_user)
        self.db.flush()
        return db_user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Obter usuário por ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Obter usuário por email."""
        return self.db.query(User).filter(User.email == email).first()

    async def list_all(self) -> List[User]:
        """Listar todos os usuários."""
        return self.db.query(User).all()

    async def update(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Atualizar usuário."""
        from app.core import get_password_hash
        
        user = await self.get_by_id(user_id)
        if not user:
            return None

        if user_update.full_name:
            user.full_name = user_update.full_name
        if user_update.password:
            user.hashed_password = get_password_hash(user_update.password)

        self.db.flush()
        return user

    async def delete(self, user_id: int) -> bool:
        """Deletar usuário."""
        user = await self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.flush()
        return True
