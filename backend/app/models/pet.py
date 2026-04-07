from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class PetTypeEnum(str, enum.Enum):
    DOG = "dog"
    CAT = "cat"

class Pet(Base):
    __tablename__ = "pets"
    
    # Índices compostos para queries comuns
    __table_args__ = (
        Index('idx_organization_created', 'organization_id', 'created_at'),
        Index('idx_type_created', 'pet_type', 'created_at'),
        Index('idx_organization_type', 'organization_id', 'pet_type'),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    pet_type = Column(SQLEnum(PetTypeEnum), default=PetTypeEnum.DOG, index=True)  # Adicionado index
    description = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations.id"), index=True, nullable=False)  # NOT NULL
    created_at = Column(DateTime, default=datetime.utcnow, index=True)  # Adicionado index
    
    # Relacionamentos com lazy loading explícito
    organization = relationship(
        "Organization", 
        back_populates="pets",
        lazy="selectin"  # MUDEI de 'select' para 'selectin' - carrega em batch
    )
    
    interest_forms = relationship(
        "InterestForm", 
        back_populates="pet", 
        cascade="all, delete-orphan",
        lazy="selectin",  # MUDEI para 'selectin' - evita N+1
        order_by="InterestForm.created_at.desc()"  # Ordenação padrão
    )