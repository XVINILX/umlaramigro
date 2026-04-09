# tests/test_registro_usuario.py
import pytest
from app.services.user_service import UserService
from app.schemas import UserCreate
from app.repositories.factory import get_user_repository
from app.repositories.factory import RepositoryFactory

@pytest.mark.asyncio
async def test_registro_usuario_com_mock():
    """Teste usando MongoDB em memória com interface assíncrona."""
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
    print(f"✅ Primeiro registro: {result1.email}")
    
    users_count = await db["users"].count_documents({})
    assert users_count == 1
    
    with pytest.raises(ValueError, match="Email already registered"):
        await user_service.register_user(user_data)

@pytest.mark.asyncio
async def test_multiplos_usuarios():
    """Teste com múltiplos usuários."""
    RepositoryFactory._backend = "mongodb"
    from app.core.mongodb import get_mongo_db
    
    db = await get_mongo_db()
    
    await db["users"].delete_many({})
    
    user_repository = await get_user_repository(db=db)
    user_service = UserService(user_repository)
    
    emails = ["user1@test.com", "user2@test.com", "user3@test.com"]
    
    for i, email in enumerate(emails, 1):
        user_data = UserCreate(
            email=email,
            full_name=f"User {i}",
            password=f"pass{i}123"
        )
        result = await user_service.register_user(user_data)
        assert result.email == email

    users_count = await db["users"].count_documents({})
    assert users_count == 3
    print(f"✅ Total de usuários: {users_count}")