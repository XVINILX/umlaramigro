from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.models.pet import Pet
from app.models.user import User


@dataclass
class InterestForm:
    """
    Entidade de domínio: Formulário de interesse em adotar.
    
    Índices recomendados para MongoDB:
    - (user_id, pet_id): Evita duplicatas de interesse do mesmo usuário no mesmo pet
    - (pet_id, created_at): Para listar formulários por pet, mais recentes primeiro
    - (user_id, created_at): Para listar formulários do usuário
    - (status, created_at): Para filtrar por status de processamento
    """
    
    id: Optional[str] = None  # MongoDB ObjectId as string
    full_name: str = ""
    phone: Optional[str] = None
    email: Optional[str] = None
    message: Optional[str] = None
    
    # Referências a outras entidades
    user_id: Optional[str] = None  # MongoDB ObjectId as string (pode ser None para não-logados)
    pet_id: Optional[str] = None   # MongoDB ObjectId as string (obrigatório)
    
    # Status do processamento da solicitação
    status: str = "pending"  # pending, contacted, adopted, rejected
    contact_date: Optional[datetime] = None
    notes: Optional[str] = None  # Notas internas
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Relacionamentos (carregados quando necessário)
    user: Optional['User'] = None
    pet: Optional['Pet'] = None