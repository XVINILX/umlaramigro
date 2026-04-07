"""Configuração de conexão com MongoDB."""
from pymongo import AsyncMongoClient
from app.core.config import settings

_mongo_client: AsyncMongoClient = None
_mongo_db: AsyncMongoClient = None
_mongo_connected = False


async def connect_to_mongo(timeout: int = 10):
    """Conectar ao MongoDB com timeout."""
    global _mongo_client, _mongo_db, _mongo_connected
    if _mongo_connected:
        return
    
    try:
        _mongo_client = AsyncMongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=timeout*1000)
        _mongo_db = _mongo_client[settings.MONGODB_DB_NAME]
        # Fazer ping com timeout
        await _mongo_client.admin.command("ping")
        _mongo_connected = True
        print("✓ Conectado ao MongoDB")
    except Exception as e:
        print(f"✗ Erro ao conectar MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Fechar conexão com MongoDB."""
    global _mongo_client, _mongo_connected
    if _mongo_client:
        _mongo_client.close()
        _mongo_connected = False
        print("✓ Desconectado do MongoDB")


async def get_mongo_db() -> AsyncMongoClient:
    """Obter instância do banco de dados MongoDB.
    
    Faz lazy loading da conexão se ainda não estiver conectado.
    """
    global _mongo_db, _mongo_connected
    if _mongo_db is None or not _mongo_connected:
        await connect_to_mongo()
    return _mongo_db
