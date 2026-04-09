"""Factory e dependências para repositórios."""
from typing import Union
from pymongo import AsyncMongoClient
from fastapi import Depends
from app.core.config import settings
from app.repositories import (
    IUserRepository,
    IOrganizationRepository,
    IPetRepository,
    IInterestFormRepository,
)
from app.repositories.mongodb_impl import (
    MongoDBUserRepository,
    MongoDBOrganizationRepository,
    MongoDBPetRepository,
    MongoDBInterestFormRepository,
)


class RepositoryFactory:
    """Factory para criar instâncias de repositórios.
    
    Suporta múltiplos backends: SQLAlchemy (PostgreSQL) e MongoDB.
    O backend é selecionado via REPOSITORY_BACKEND no settings.
    """

    _backend = getattr(settings, "REPOSITORY_BACKEND", "sqlalchemy")

    @classmethod
    def set_backend(cls, backend: str):
        """Define qual backend usar: 'sqlalchemy' ou 'mongodb'."""
        if backend not in ["sqlalchemy", "mongodb"]:
            raise ValueError("Backend deve ser 'sqlalchemy' ou 'mongodb'")
        cls._backend = backend

    @staticmethod
    def get_user_repository(db: Union[AsyncMongoClient]):
        """Retorna instância do repositório de usuários."""
        if RepositoryFactory._backend == "mongodb":
            print("Criando MongoDBUserRepository")
            return MongoDBUserRepository(db)
        print('terminando get_user_repository')

    @staticmethod
    def get_organization_repository(db: Union[AsyncMongoClient]):
        """Retorna instância do repositório de organizações."""
        if RepositoryFactory._backend == "mongodb":
            return MongoDBOrganizationRepository(db)

    @staticmethod
    def get_pet_repository(db: Union[AsyncMongoClient]):
        """Retorna instância do repositório de pets."""
        if RepositoryFactory._backend == "mongodb":
            return MongoDBPetRepository(db)

    @staticmethod
    def get_interest_form_repository(db: Union[AsyncMongoClient]):
        """Retorna instância do repositório de formulários de interesse."""
        if RepositoryFactory._backend == "mongodb":
            return MongoDBInterestFormRepository(db)


# Dependências de banco de dados - retorna o db correto baseado no backend configurado
async def _get_db_dependency():
    """Dependency interna que retorna o banco de dados correto."""
    if RepositoryFactory._backend == "mongodb":
        from app.core.mongodb import get_mongo_db
        db = await get_mongo_db()
        yield db



# Dependências para injeção no FastAPI
async def get_user_repository(
    db: Union[AsyncMongoClient] = Depends(_get_db_dependency)
) -> IUserRepository:
    """Dependency para injetar repositório de usuários."""
    return RepositoryFactory.get_user_repository(db)


async def get_organization_repository(
    db: Union[AsyncMongoClient] = Depends(_get_db_dependency)
) -> IOrganizationRepository:
    """Dependency para injetar repositório de organizações."""
    return RepositoryFactory.get_organization_repository(db)


async def get_pet_repository(
    db: Union[AsyncMongoClient] = Depends(_get_db_dependency)
) -> IPetRepository:
    """Dependency para injetar repositório de pets."""
    return RepositoryFactory.get_pet_repository(db)


async def get_interest_form_repository(
    db: Union[AsyncMongoClient] = Depends(_get_db_dependency)
) -> IInterestFormRepository:
    """Dependency para injetar repositório de formulários de interesse."""
    return RepositoryFactory.get_interest_form_repository(db)

