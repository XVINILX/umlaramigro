# tests/test_registro_usuario.py
import pytest
from app.services.user_service import UserService
from app.schemas import UserCreate
from app.repositories.factory import get_user_repository
from app.repositories.factory import RepositoryFactory

@pytest.mark.asyncio
async def test_login_usuario_sucesso_com_mock():
    # Configurar o backend
    RepositoryFactory._backend = "mongodb"
    
    from app.core.mongodb import get_mongo_db
    
    db = await get_mongo_db()
    
    # Agora podemos usar await normalmente
    users_count = await db["users"].count_documents({})
    assert users_count == 0
    
    user_repository = await get_user_repository(db=db)
    user_service = UserService(user_repository)
    
    user_data = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="testpassword"
    )
    
    result1 = await user_service.register_user(user_data)

    usuario_logado = await user_service.authenticate_user(
        email=user_data.email,
        password=user_data.password)
    
    assert usuario_logado is not None


@pytest.mark.asyncio
async def test_login_usuario_senha_errada_com_mock():
    # Configurar o backend
    RepositoryFactory._backend = "mongodb"
    
    from app.core.mongodb import get_mongo_db
    
    db = await get_mongo_db()
    
    # Agora podemos usar await normalmente
    users_count = await db["users"].count_documents({})
    assert users_count == 0
    
    user_repository = await get_user_repository(db=db)
    user_service = UserService(user_repository)
    
    user_data = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="testpassword"
    )
    
    result1 = await user_service.register_user(user_data)

    usuario_logado = await user_service.authenticate_user(
        email=user_data.email,
        password='user_data.password')
    
    assert usuario_logado is None


@pytest.mark.asyncio
async def test_login_usuario_email_errado_com_mock():
    # Configurar o backend
    RepositoryFactory._backend = "mongodb"
    
    from app.core.mongodb import get_mongo_db
    
    db = await get_mongo_db()
    
    # Agora podemos usar await normalmente
    users_count = await db["users"].count_documents({})
    assert users_count == 0
    
    user_repository = await get_user_repository(db=db)
    user_service = UserService(user_repository)
    
    user_data = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="testpassword"
    )
    
    result1 = await user_service.register_user(user_data)

    usuario_logado = await user_service.authenticate_user(
        email='user_data.email',
        password=user_data.password)
    
    assert usuario_logado is None