from app.core import verify_password
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.repositories import IUserRepository
from app.schemas.user import UserResponse


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """
        Register a new user with business validation.
        Raises:
            ValueError: If email is already registered
        """
        # Verificação de email duplicado
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        return await self.create_user(user_data)
    
    async def create_user(self, user: UserCreate) -> User:
        return await self.user_repo.create(user)

    async def get_user_by_email(self, email: str) -> User:
        return await self.user_repo.get_by_email(email)

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.user_repo.get_by_id(user_id)

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    async def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        return await self.user_repo.update(user_id, user_update)

    async def list_users(self) -> list:
        return await self.user_repo.list_all()
