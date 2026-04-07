from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class InterestForm(Base):
    __tablename__ = "interest_forms"
    
    # Índices compostos para queries comuns
    __table_args__ = (
        Index('ix_interest_forms_user_pet', 'user_id', 'pet_id'),  # Evita duplicatas
        Index('ix_interest_forms_pet_created', 'pet_id', 'created_at'),  # Para listar por pet
        Index('ix_interest_forms_user_created', 'user_id', 'created_at'),  # Para listar por user
        Index('ix_interest_forms_status_created', 'status', 'created_at'),  # Para filtros
    )

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)  # NOT NULL
    phone = Column(String, nullable=True, index=True)  # Adicionado index para busca
    email = Column(String, nullable=True, index=True)  # ADICIONADO - campo essencial para contato
    message = Column(Text,nullable=True)  # ADICIONADO - para mensagem do interessado
    
    # Foreign keys com CASCADE apropriado
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=True)  # NULL permitido para não-logados
    pet_id = Column(Integer, ForeignKey("pets.id", ondelete="CASCADE"), index=True, nullable=False)  # NOT NULL
    
    # Status para workflow
    status = Column(String, default="pending", index=True)  # pending, contacted, adopted, rejected
    contact_date = Column(DateTime, nullable=True)  # Quando foi contatado
    notes = Column(Text, nullable=True)  # Notas internas
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos otimizados
    user = relationship(
        "User", 
        back_populates="interest_forms",
        lazy="selectin",  # Muda de 'select' para 'selectin'
        foreign_keys=[user_id]
    )
    
    pet = relationship(
        "Pet", 
        back_populates="interest_forms",
        lazy="selectin",  # Muda de 'select' para 'selectin'
        foreign_keys=[pet_id]
    )