from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Organization(Base):
    __tablename__ = "organizations"
    
    # Índices compostos para queries comuns
    __table_args__ = (
        Index('ix_organizations_owner_created', 'owner_id', 'created_at'),
        Index('ix_organizations_name_owner', 'name', 'owner_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)  # NOT NULL
    description = Column(Text)  # Mudei de String para Text (mais eficiente para textos longos)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)  # NOT NULL + CASCADE
    created_at = Column(DateTime, default=datetime.utcnow, index=True)  # Adicionado index
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Para tracking
    
    # Relacionamentos otimizados
    owner = relationship(
        "User", 
        back_populates="organizations",
        lazy="selectin",  # Muda de 'select' para 'selectin'
        foreign_keys=[owner_id]
    )
    
    pets = relationship(
        "Pet", 
        back_populates="organization", 
        cascade="all, delete-orphan",
        lazy="selectin",  # CRÍTICO: muda de 'select' para 'selectin'
        order_by="Pet.created_at.desc()"  # Ordenação padrão
    )