from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Organization:
    """
    Entidade de domínio: Organização/Abrigo de animais.
    
    Índices recomendados para MongoDB:
    - (owner_id, created_at): Para listar organizações por proprietário
    - (name, owner_id): Para busca por nome dentro de um proprietário
    """
    
    id: Optional[str] = None  # MongoDB ObjectId as string
    name: str = ""
    description: Optional[str] = None
    owner_id: Optional[str] = None  # Referência ao User
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Relacionamentos (carregados quando necessário)
    owner: Optional['User'] = None
    pets: List['Pet'] = field(default_factory=list)