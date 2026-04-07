"""
Configurações e fixtures compartilhadas para testes pytest.

Use fixtures aqui para serem reutilizadas em todos os testes.
"""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, get_db


# ============ FIXTURES ============

@pytest.fixture(scope="session")
def test_db():
    """
    Cria banco de dados de teste para a sessão inteira.
    
    Usa SQLite em memória por padrão (rápido).
    """
    # Use a variável de ambiente se definida, caso contrário SQLite em memória
    database_url = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")
    
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
    )
    
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Limpa após testes
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    """
    Fornece uma sessão de banco de dados para cada teste.
    """
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    
    session = TestingSessionLocal()
    
    # Override dependency
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield session
    
    # Limpa banco após cada teste
    session.rollback()
    session.close()
    
    app.dependency_overrides.clear()


@pytest.fixture
def client(db_session):
    """
    Fornece um cliente HTTP de teste com DB mockado.
    """
    return TestClient(app)


@pytest.fixture
def authenticated_client(client, db_session):
    """
    Fornece um cliente HTTP autenticado (com token JWT).
    
    Nota: Implemente conforme sua estratégia de auth.
    """
    # Cria usuário de teste
    # user = User(email="test@example.com", ...)
    # db_session.add(user)
    # db_session.commit()
    
    # Faz login para obter token
    # response = client.post("/auth/login", json={"username": "test@example.com", "password": "..."})
    # token = response.json()["access_token"]
    
    # Seta header de autorização
    # client.headers = {"Authorization": f"Bearer {token}"}
    
    return client


# ============ MARKERS CUSTOMIZADOS ============

def pytest_configure(config):
    """Registra marcadores customizados."""
    config.addinivalue_line(
        "markers", "slow: marca teste como lento"
    )
    config.addinivalue_line(
        "markers", "integration: marca teste como integração"
    )
    config.addinivalue_line(
        "markers", "unit: marca teste como unitário"
    )


# ============ HOOKS ============

def pytest_collection_modifyitems(config, items):
    """
    Adiciona marcadores automáticos baseado no nome do arquivo.
    """
    for item in items:
        # test_units.py -> @pytest.mark.unit
        if "unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        # test_integration.py -> @pytest.mark.integration
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
