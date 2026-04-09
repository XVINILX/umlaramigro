# tests/test_auth_e2e.py
import pytest

@pytest.mark.asyncio
async def test_login_organizacao_success(e2e_mock_db, client):
    response = client.post(
        "/auth/register",
        json={
            "email": "success@example.com",
            "full_name": "Success User",
            "password": "securepass123"
        }
    )

    token_usuario = client.post(
        "/auth/login",
        json={
            "email": "success@example.com",
            "password": "securepass123"
        }
    )

    response_json = token_usuario.json()
    assert response_json['access_token'] is not None    

