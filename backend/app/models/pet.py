from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List


class PetType(str, Enum):
    """Tipos de animais suportados."""
    DOG = "dog"
    CAT = "cat"


@dataclass
class Pet:
    """
    Entidade de domínio: Animal de estimação.
    
    Índices recomendados para MongoDB:
    - (organization_id, created_at): Para listar pets por organização
    - (pet_type, created_at): Para filtrar por tipo de animal
    - (organization_id, pet_type): Para buscar tipo específico em organização
    """
    
    id: Optional[str] = None  # MongoDB ObjectId as string
    name: str = ""
    pet_type: PetType = PetType.DOG
    description: Optional[str] = None
    organization_id: Optional[str] = None  # Referência à Organization
    created_at: Optional[datetime] = None
    
    # Relacionamentos (carregados quando necessário)
    organization: Optional['Organization'] = None
    interest_forms: List['InterestForm'] = field(default_factory=list)