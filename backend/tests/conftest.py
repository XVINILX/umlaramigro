# tests/conftest.py
from fastapi.testclient import TestClient
import pytest
from mongomock import MongoClient
from unittest.mock import AsyncMock
from app.main import app
from app.repositories.factory import get_user_repository
from app.repositories.mongodb_impl import MongoDBUserRepository

# tests/conftest.py
class AsyncMockCursor:
    """Mock de cursor assíncrono para suportar async for."""
    
    def __init__(self, documents):
        self._documents = documents
        self._index = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self._index >= len(self._documents):
            raise StopAsyncIteration
        doc = self._documents[self._index]
        self._index += 1
        return doc
    
    async def to_list(self, length=None):
        """Suporte ao método to_list."""
        if length is None:
            return self._documents
        return self._documents[:length]

class AsyncMongoCollection:
    """Wrapper que transforma chamadas síncronas do mongomock em assíncronas."""
    
    def __init__(self, collection):
        self._collection = collection
    
    async def count_documents(self, filter_dict=None):
        """Versão assíncrona do count_documents."""
        if filter_dict is None:
            filter_dict = {}
        return self._collection.count_documents(filter_dict)
    
    async def find_one(self, filter_dict):
        """Versão assíncrona do find_one."""
        return self._collection.find_one(filter_dict)
    
    async def insert_one(self, document):
        """Versão assíncrona do insert_one."""
        return self._collection.insert_one(document)
    
    async def delete_many(self, filter_dict):
        """Versão assíncrona do delete_many."""
        return self._collection.delete_many(filter_dict)
    
    def find(self, filter_dict=None):  # ← Síncrono
        """Versão síncrona do find - retorna um cursor mockado."""
        if filter_dict is None:
            filter_dict = {}
        
        # Busca os documentos (síncrono)
        cursor = self._collection.find(filter_dict)
        documents = list(cursor)
        
        # Retorna um cursor mockado que suporta async for
        return AsyncMockCursor(documents)
    
    def __getattr__(self, name):
        """Para outros métodos, retorna o original (mas sem await)."""
        return getattr(self._collection, name)

class AsyncMongoDatabase:
    """Wrapper assíncrono para o banco de dados."""
    
    def __init__(self, db):
        self._db = db
    
    def __getitem__(self, name):
        """Retorna uma coleção assíncrona."""
        return AsyncMongoCollection(self._db[name])
    
    async def list_collection_names(self):
        """Versão assíncrona do list_collection_names."""
        return self._db.list_collection_names()

@pytest.fixture
async def mock_mongodb():
    """Usa MongoDB em memória com interface assíncrona."""
    client = MongoClient()
    db = AsyncMongoDatabase(client["test_database"])
    
    for collection_name in await db.list_collection_names():
        await db[collection_name].delete_many({})
    
    yield db
    
    client.close()

@pytest.fixture(autouse=True)
async def setup_test_db(mock_mongodb):
    """Substitui o banco real pelo mock assíncrono."""
    from app.core import mongodb
    
    original_get_db = mongodb.get_mongo_db
    
    async def mock_get_db():
        return mock_mongodb
    
    mongodb.get_mongo_db = mock_get_db
    
    yield
    
    # Restaura a função original
    mongodb.get_mongo_db = original_get_db



@pytest.fixture
async def e2e_mock_db(mock_mongodb):
    """Prepara o ambiente para testes E2E."""
    # Garantir que o banco está limpo
    await mock_mongodb["users"].delete_many({})
    
    # Criar repositório mockado
    repo = MongoDBUserRepository(mock_mongodb)
    
    # Salvar overrides originais
    original_overrides = app.dependency_overrides.copy()
    
    # Aplicar override
    app.dependency_overrides[get_user_repository] = lambda: repo
    
    yield mock_mongodb
    
    # Restaurar
    app.dependency_overrides.clear()
    app.dependency_overrides.update(original_overrides)

@pytest.fixture
def client():
    """Cliente de teste FastAPI."""
    return TestClient(app)