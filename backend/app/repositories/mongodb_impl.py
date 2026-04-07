from typing import Optional, List, Tuple
from datetime import datetime
from bson import ObjectId
from pymongo import AsyncMongoClient
from app.models import User, Organization, Pet, InterestForm
from app.schemas import (
    UserCreate, UserUpdate, OrganizationCreate, OrganizationUpdate,
    PetCreate, PetUpdate, InterestFormCreate
)
from app.repositories import (
    IUserRepository, IOrganizationRepository, IPetRepository, IInterestFormRepository
)
from app.core import get_password_hash, verify_password


class MongoModelWrapper:
    """Wrapper para permitir que objetos MongoDB sejam serializados por FastAPI como Pydantic models."""
    def __init__(self, data: dict):
        self.__dict__.update(data)


def _convert_mongo_doc_to_user_dict(doc: dict) -> dict:
    """Converter documento MongoDB para dict compatível com modelo User."""
    return {
        "id": str(doc.get("_id")),
        "email": doc.get("email"),
        "full_name": doc.get("full_name"),
        "hashed_password": doc.get("hashed_password"),
        "is_active": doc.get("is_active", True),
        "created_at": doc.get("created_at", datetime.utcnow()),
        "updated_at": doc.get("updated_at", datetime.utcnow()),
    }


def _convert_mongo_doc_to_org_dict(doc: dict) -> dict:
    """Converter documento MongoDB para dict compatível com modelo Organization."""
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "description": doc.get("description"),
        "owner_id": str(doc.get("owner_id")) if doc.get("owner_id") else None,
        "created_at": doc.get("created_at", datetime.utcnow()),
    }


def _convert_mongo_doc_to_pet_dict(doc: dict) -> dict:
    """Converter documento MongoDB para dict compatível com modelo Pet."""
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "pet_type": doc.get("pet_type"),
        "description": doc.get("description"),
        "organization_id": str(doc.get("organization_id")) if doc.get("organization_id") else None,
        "created_at": doc.get("created_at", datetime.utcnow()),
    }


def _convert_mongo_doc_to_form_dict(doc: dict) -> dict:
    """Converter documento MongoDB para dict compatível com modelo InterestForm."""
    return {
        "id": str(doc.get("_id")),
        "full_name": doc.get("full_name"),
        "phone": doc.get("phone"),
        "user_id": str(doc.get("user_id")) if doc.get("user_id") else None,
        "pet_id": str(doc.get("pet_id")) if doc.get("pet_id") else None,
        "created_at": doc.get("created_at", datetime.utcnow()),
    }


def _convert_mongo_to_user_wrapper(doc: dict):
    """Converter documento MongoDB para objeto serializável como User."""
    data = _convert_mongo_doc_to_user_dict(doc)
    return MongoModelWrapper(data)


def _convert_mongo_to_org_wrapper(doc: dict):
    """Converter documento MongoDB para objeto serializável como Organization."""
    data = _convert_mongo_doc_to_org_dict(doc)
    return MongoModelWrapper(data)


def _convert_mongo_to_pet_wrapper(doc: dict):
    """Converter documento MongoDB para objeto serializável como Pet."""
    data = _convert_mongo_doc_to_pet_dict(doc)
    return MongoModelWrapper(data)


def _convert_mongo_to_form_wrapper(doc: dict):
    """Converter documento MongoDB para objeto serializável como InterestForm."""
    data = _convert_mongo_doc_to_form_dict(doc)
    return MongoModelWrapper(data)


class MongoDBUserRepository(IUserRepository):
    """Implementação MongoDB do repositório de usuários."""

    def __init__(self, db: AsyncMongoClient):
        self.db = db
        self.collection = db["users"]

    async def create(self, user: UserCreate) -> User:
        """Criar um novo usuário."""
        hashed_password = get_password_hash(user.password)
        now = datetime.utcnow()
        user_dict = {
            "email": user.email,
            "full_name": user.full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }
        result = await self.collection.insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        return User(**_convert_mongo_doc_to_user_dict(user_dict))

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Obter usuário por ID."""
        try:
            user = await self.collection.find_one({"_id": ObjectId(str(user_id))})
            if user:
                return _convert_mongo_to_user_wrapper(user)
        except Exception:
            pass
        return None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Obter usuário por email."""
        user = await self.collection.find_one({"email": email})
        if user:
            return _convert_mongo_to_user_wrapper(user)
        return None

    async def list_all(self) -> List[User]:
        """Listar todos os usuários."""
        users = []
        async for user in self.collection.find():
            users.append(_convert_mongo_to_user_wrapper(user))
        return users

    async def update(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Atualizar usuário."""
        update_data = {}
        if user_update.full_name:
            update_data["full_name"] = user_update.full_name
        if user_update.password:
            update_data["hashed_password"] = get_password_hash(user_update.password)

        if update_data:
            update_data["updated_at"] = datetime.utcnow()

        if not update_data:
            return await self.get_by_id(user_id)

        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(str(user_id))},
                {"$set": update_data}
            )
            if result.matched_count == 0:
                return None
        except Exception:
            return None

        return await self.get_by_id(user_id)

    async def delete(self, user_id: int) -> bool:
        """Deletar usuário."""
        try:
            result = await self.collection.delete_one(
                {"_id": ObjectId(str(user_id))}
            )
            return result.deleted_count > 0
        except Exception:
            return False


class MongoDBOrganizationRepository(IOrganizationRepository):
    """Implementação MongoDB do repositório de organizações."""

    def __init__(self, db: AsyncMongoClient):
        self.db = db
        self.collection = db["organizations"]

    async def create(self, org: OrganizationCreate, owner_id: int) -> Organization:
        """Criar uma nova organização."""
        now = datetime.utcnow()
        org_dict = {
            "name": org.name,
            "description": org.description,
            "owner_id": owner_id,
            "created_at": now,
        }
        result = await self.collection.insert_one(org_dict)
        org_dict["_id"] = result.inserted_id
        return _convert_mongo_to_org_wrapper(org_dict)

    async def get_by_id(self, org_id: int) -> Optional[Organization]:
        """Obter organização por ID."""
        try:
            org = await self.collection.find_one({"_id": ObjectId(str(org_id))})
            if org:
                return _convert_mongo_to_org_wrapper(org)
        except Exception:
            pass
        return None

    async def get_by_owner(self, owner_id: int) -> List[Organization]:
        """Obter organizações de um proprietário."""
        orgs = []
        async for org in self.collection.find({"owner_id": owner_id}):
            orgs.append(_convert_mongo_to_org_wrapper(org))
        return orgs

    async def list_all(self) -> List[Organization]:
        """Listar todas as organizações."""
        orgs = []
        async for org in self.collection.find():
            orgs.append(_convert_mongo_to_org_wrapper(org))
        return orgs

    async def update(self, org_id: int, org_update: OrganizationUpdate) -> Optional[Organization]:
        """Atualizar organização."""
        update_data = {}
        if org_update.name:
            update_data["name"] = org_update.name
        if org_update.description:
            update_data["description"] = org_update.description

        if not update_data:
            return await self.get_by_id(org_id)

        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(str(org_id))},
                {"$set": update_data}
            )
            if result.matched_count == 0:
                return None
        except Exception:
            return None

        return await self.get_by_id(org_id)

    async def delete(self, org_id: int) -> bool:
        """Deletar organização."""
        try:
            result = await self.collection.delete_one(
                {"_id": ObjectId(str(org_id))}
            )
            return result.deleted_count > 0
        except Exception:
            return False


class MongoDBPetRepository(IPetRepository):
    """Implementação MongoDB do repositório de pets."""

    def __init__(self, db: AsyncMongoClient):
        self.db = db
        self.collection = db["pets"]

    async def create(self, pet: PetCreate, organization_id: int) -> Pet:
        """Criar um novo pet."""
        now = datetime.utcnow()
        pet_dict = {
            "name": pet.name,
            "pet_type": pet.pet_type,
            "description": pet.description,
            "organization_id": organization_id,
            "created_at": now,
        }
        result = await self.collection.insert_one(pet_dict)
        pet_dict["_id"] = result.inserted_id
        return _convert_mongo_to_pet_wrapper(pet_dict)

    async def get_by_id(self, pet_id: int) -> Optional[Pet]:
        """Obter pet por ID."""
        try:
            pet = await self.collection.find_one({"_id": ObjectId(str(pet_id))})
            if pet:
                return _convert_mongo_to_pet_wrapper(pet)
        except Exception:
            pass
        return None

    async def get_by_organization(self, organization_id: int) -> List[Pet]:
        """Obter pets de uma organização."""
        pets = []
        async for pet in self.collection.find({"organization_id": organization_id}):
            pets.append(_convert_mongo_to_pet_wrapper(pet))
        return pets

    async def list_all(self) -> List[Pet]:
        """Listar todos os pets."""
        pets = []
        async for pet in self.collection.find():
            pets.append(_convert_mongo_to_pet_wrapper(pet))
        return pets

    async def update(self, pet_id: int, pet_update: PetUpdate) -> Optional[Pet]:
        """Atualizar pet."""
        update_data = {}
        if pet_update.name:
            update_data["name"] = pet_update.name
        if pet_update.description:
            update_data["description"] = pet_update.description

        if not update_data:
            return await self.get_by_id(pet_id)

        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(str(pet_id))},
                {"$set": update_data}
            )
            if result.matched_count == 0:
                return None
        except Exception:
            return None

        return await self.get_by_id(pet_id)

    async def delete(self, pet_id: int) -> bool:
        """Deletar pet."""
        try:
            result = await self.collection.delete_one(
                {"_id": ObjectId(str(pet_id))}
            )
            return result.deleted_count > 0
        except Exception:
            return False


class MongoDBInterestFormRepository(IInterestFormRepository):
    """Implementação MongoDB do repositório de formulários de interesse."""

    def __init__(self, db: AsyncMongoClient):
        self.db = db
        self.collection = db["interest_forms"]

    async def create(self, form: InterestFormCreate, user_id: int, pet_id: int) -> InterestForm:
        """Criar um novo formulário de interesse."""
        form_dict = {
            "full_name": form.full_name,
            "phone": form.phone,
            "user_id": user_id,
            "pet_id": pet_id,
            "created_at": datetime.utcnow(),
        }
        result = await self.collection.insert_one(form_dict)
        form_dict["_id"] = result.inserted_id
        return _convert_mongo_to_form_wrapper(form_dict)

    async def get_by_id(self, form_id: int) -> Optional[InterestForm]:
        """Obter formulário por ID."""
        try:
            form = await self.collection.find_one({"_id": ObjectId(str(form_id))})
            if form:
                return _convert_mongo_to_form_wrapper(form)
        except Exception:
            pass
        return None

    async def get_by_pet(self, pet_id: int) -> List[InterestForm]:
        """Obter formulários de um pet."""
        forms = []
        async for form in self.collection.find({"pet_id": pet_id}):
            forms.append(_convert_mongo_to_form_wrapper(form))
        return forms

    async def get_by_user(self, user_id: int) -> List[InterestForm]:
        """Obter formulários de um usuário."""
        forms = []
        async for form in self.collection.find({"user_id": user_id}):
            forms.append(_convert_mongo_to_form_wrapper(form))
        return forms

    async def list_all(self) -> List[InterestForm]:
        """Listar todos os formulários."""
        forms = []
        async for form in self.collection.find():
            forms.append(_convert_mongo_to_form_wrapper(form))
        return forms

    async def delete(self, form_id: int) -> bool:
        """Deletar formulário."""
        try:
            result = await self.collection.delete_one(
                {"_id": ObjectId(str(form_id))}
            )
            return result.deleted_count > 0
        except Exception:
            return False

    async def get_with_details(self, pet_id: int) -> List[Tuple]:
        """Obter formulários com detalhes de pet e organização."""
        # MongoDB lookup com agregação
        pipeline = [
            {"$match": {"pet_id": pet_id}},
            {
                "$lookup": {
                    "from": "pets",
                    "localField": "pet_id",
                    "foreignField": "_id",
                    "as": "pet"
                }
            },
            {
                "$lookup": {
                    "from": "organizations",
                    "localField": "pet.organization_id",
                    "foreignField": "_id",
                    "as": "organization"
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "full_name": 1,
                    "phone": 1,
                    "user_id": 1,
                    "pet_id": 1,
                    "created_at": 1,
                    "pet_name": {"$arrayElemAt": ["$pet.name", 0]},
                    "org_name": {"$arrayElemAt": ["$organization.name", 0]},
                }
            }
        ]

        results = []
        try:
            async for doc in self.collection.aggregate(pipeline):
                form_data = _convert_mongo_doc_to_form_dict(doc)
                form = _convert_mongo_to_form_wrapper(doc)
                results.append((form, doc.get("pet_name"), doc.get("org_name")))
        except Exception:
            pass

        return results
