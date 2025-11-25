from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True)
    vip = Column(Boolean, nullable=False, server_default="0")
    
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")