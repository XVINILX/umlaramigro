from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    # Índices compostos para queries comuns
    __table_args__ = (
        Index('ix_users_active_created', 'is_active', 'created_at'),
        Index('ix_users_email_active', 'email', 'is_active'),  # Para login com verificação de ativo
    )

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)  # NOT NULL
    full_name = Column(String, nullable=False)  # NOT NULL
    hashed_password = Column(String, nullable=False)  # NOT NULL
    is_active = Column(Boolean, default=True, index=True)  # Adicionado index
    created_at = Column(DateTime, default=datetime.utcnow, index=True)  # Adicionado index
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Útil para tracking
    
    # Relacionamentos otimizados
    organizations = relationship(
        "Organization", 
        back_populates="owner",
        lazy="selectin",  # Muda de 'select' para 'selectin'
        cascade="all, delete-orphan"  # Remove organizações quando user for deletado
    )
    
    interest_forms = relationship(
        "InterestForm", 
        back_populates="user",
        lazy="selectin",  # Muda de 'select' para 'selectin'
        order_by="InterestForm.created_at.desc()"  # Mais recentes primeiro
    )