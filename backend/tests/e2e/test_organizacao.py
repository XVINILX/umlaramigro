# tests/test_auth_e2e.py
import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_criar_organizacao_success(e2e_mock_db, client):
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
    header = {"Authorization": "Bearer " + response_json['access_token']}
    
    dados_criar_organizacao = {
        "name": "Organização de Teste",
        "description": "Descrição da organização de teste"  
    }

    response = client.post("/organizations/", json=dados_criar_organizacao, headers=header) 

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json['name'] == dados_criar_organizacao['name']
    assert response_json['description'] == dados_criar_organizacao['description']

@pytest.mark.asyncio
async def test_criar_organizacao_unauthorized(client):
    dados_criar_organizacao = {
        "name": "Organização de Teste",
        "description": "Descrição da organização de teste"  
    }

    response = client.post("/organizations/", json=dados_criar_organizacao) 

    assert response.status_code == status.HTTP_403_FORBIDDEN 

@pytest.mark.asyncio
async def test_listar_minha_organizacao_success(e2e_mock_db, client):
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
    header = {"Authorization": "Bearer " + response_json['access_token']}
    
    dados_criar_organizacao = {
        "name": "Organização de Teste",
        "description": "Descrição da organização de teste"  
    }

    response = client.post("/organizations/", json=dados_criar_organizacao, headers=header) 

    response = client.get("/organizations/my-organizations", headers=header)

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]['name'] == dados_criar_organizacao['name']
    assert response_json[0]['description'] == dados_criar_organizacao['description']

@pytest.mark.asyncio
async def test_listar_minha_organizacao_erro(e2e_mock_db, client):
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
    header = {"Authorization": "Bearer " + response_json['access_token']}
    
    dados_criar_organizacao = {
        "name": "Organização de Teste",
        "description": "Descrição da organização de teste"  
    }

    response = client.post("/organizations/", json=dados_criar_organizacao, headers=header) 

    response = client.get("/organizations/my-organizations", headers=header)

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]['name'] == dados_criar_organizacao['name']
    assert response_json[0]['description'] == dados_criar_organizacao['description']


    response = client.post(
        "/auth/register",
        json={
            "email": "success2@example.com",
            "full_name": "Success User",
            "password": "securepass123"
        }
    )

    token_usuario = client.post(
        "/auth/login",
        json={
            "email": "success2@example.com",
            "password": "securepass123"
        }
    )

    response_json = token_usuario.json()
    header = {"Authorization": "Bearer " + response_json['access_token']}

    response = client.get("/organizations/my-organizations", headers=header)
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert len(response_json) == 0

@pytest.mark.asyncio
async def test_listar_todas_organizacoes_sem_auth(e2e_mock_db, client):
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
    header = {"Authorization": "Bearer " + response_json['access_token']}
    
    dados_criar_organizacao = {
        "name": "Organização de Teste",
        "description": "Descrição da organização de teste"  
    }
    response = client.post("/organizations/", json=dados_criar_organizacao, headers=header) 


    dados_criar_organizacao = {
        "name": "Organização2 de Teste",
        "description": "Descrição da organização de teste"  
    }

    response = client.post("/organizations/", json=dados_criar_organizacao, headers=header) 
    
    response = client.get("/organizations/") 
    response_json = response.json()
    assert len(response_json) == 2


@pytest.mark.asyncio
async def test_put_organizacao_success(e2e_mock_db, client):
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
    header = {"Authorization": "Bearer " + response_json['access_token']}
    
    dados_criar_organizacao = {
        "name": "Organização de Teste",
        "description": "Descrição da organização de teste"  
    }

    response = client.post("/organizations/", json=dados_criar_organizacao, headers=header) 

    dados_criar_organizacao_alterado = {
        "name": "Alteração Organização de Teste",
        "description": "Descrição da organização de teste"  
    }

    response = client.put("/organizations/" + str(response.json()['id']), json=dados_criar_organizacao_alterado, headers=header) 
    response.raise_for_status()
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json['name'] == dados_criar_organizacao_alterado['name']
    assert response_json['description'] == dados_criar_organizacao_alterado['description']



@pytest.mark.asyncio
async def test_put_outro_usuario_erro(e2e_mock_db, client):
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
    header = {"Authorization": "Bearer " + response_json['access_token']}
    
    dados_criar_organizacao = {
        "name": "Organização de Teste",
        "description": "Descrição da organização de teste"  
    }

    response_criar_organizacao = client.post("/organizations/", json=dados_criar_organizacao, headers=header) 


    response = client.post(
        "/auth/register",
        json={
            "email": "success2@example.com",
            "full_name": "Success User",
            "password": "securepass123"
        }
    )

    token_usuario = client.post(
        "/auth/login",
        json={
            "email": "success2@example.com",
            "password": "securepass123"
        }
    )

    response_json = token_usuario.json()
    header = {"Authorization": "Bearer " + response_json['access_token']}

    dados_criar_organizacao_alterado = {
        "name": "Alteração Organização de Teste",
        "description": "Descrição da organização de teste"  
    }

    response = client.put("/organizations/" + str(response_criar_organizacao.json()['id']), json=dados_criar_organizacao_alterado, headers=header) 

    assert response.status_code == status.HTTP_403_FORBIDDEN 