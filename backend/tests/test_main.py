"""
Testes para o módulo principal (app.main).
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthCheck:
    """Suite de testes para health check."""
    
    def test_health_check_returns_ok(self, client: TestClient):
        """Testa se health check retorna status healthy."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    @pytest.mark.slow
    def test_health_check_performance(self, client: TestClient):
        """Testa performance do health check (deve ser < 10ms)."""
        import time
        
        start = time.time()
        response = client.get("/health")
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 0.01  # 10ms


class TestRootEndpoint:
    """Suite de testes para endpoint raiz."""
    
    def test_root_returns_welcome_message(self, client: TestClient):
        """Testa se root endpoint retorna mensagem de boas-vindas."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Welcome to UmlAramigo API"
    
    def test_root_includes_documentation_links(self, client: TestClient):
        """Testa se root inclui links para documentação."""
        response = client.get("/")
        data = response.json()
        
        assert "docs" in data
        assert "redoc" in data
        assert data["docs"] == "/docs"
