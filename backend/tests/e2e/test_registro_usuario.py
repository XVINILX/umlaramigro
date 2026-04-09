# tests/test_auth_e2e.py
import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_register_success(e2e_mock_db, client):
    """Teste E2E: registro bem sucedido."""
    
    response = client.post(
        "/auth/register",
        json={
            "email": "success@example.com",
            "full_name": "Success User",
            "password": "securepass123"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "success@example.com"
    
    # Verificar no banco
    user = await e2e_mock_db["users"].find_one({"email": "success@example.com"})
    assert user is not None

@pytest.mark.asyncio
async def test_register_duplicate_email(e2e_mock_db, client):
    """Teste E2E: tentar registrar email duplicado."""
    
    # Primeiro registro
    response1 = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "full_name": "First User",
            "password": "pass123"
        }
    )
    assert response1.status_code == 200
    
    # Segundo registro com mesmo email
    response2 = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "full_name": "Second User",
            "password": "pass456"
        }
    )
    
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response2.text

@pytest.mark.asyncio
async def test_register_invalid_email(e2e_mock_db, client):
    """Teste E2E: email inválido."""
    
    response = client.post(
        "/auth/register",
        json={
            "email": "invalid-email",
            "full_name": "Test User",
            "password": "pass123"
        }
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY