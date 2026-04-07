from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from app.core import create_access_token, settings
from app.utils.dependencies import get_current_user
from app.schemas import UserCreate, UserLogin, UserResponse
from app.services import UserService
from app.repositories import IUserRepository
from app.repositories.factory import get_user_repository

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
async def register(
    user: UserCreate,
    user_repo: IUserRepository = Depends(get_user_repository),
):
    """Register a new user."""
    try:
        user_service = UserService(user_repo)
        existing_user = await user_service.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        new_user = await user_service.create_user(user)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.post("/login")
async def login(
    credentials: UserLogin,
    user_repo: IUserRepository = Depends(get_user_repository),
):
    """Login user and return access token."""
    try:
        user_service = UserService(user_repo)
        user = await user_service.authenticate_user(credentials.email, credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.from_orm(user),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
