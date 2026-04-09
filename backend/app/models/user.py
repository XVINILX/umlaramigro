from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class User:
    """
    Entidade de domínio: Usuário do sistema.
    
    Índices recomendados para MongoDB:
    - (is_active, created_at): Para filtrar usuários ativos por data
    - (email, is_active): Para autenticação com verificação de status
    """
    
    id: Optional[str] = None  # MongoDB ObjectId as string
    email: str = ""
    full_name: str = ""
    hashed_password: str = ""
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Relacionamentos (carregados quando necessário)
    organizations: List['Organization'] = field(default_factory=list)
    interest_forms: List['InterestForm'] = field(default_factory=list)