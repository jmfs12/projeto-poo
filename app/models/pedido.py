from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=True) 
    entregue = Column(Boolean, nullable=False, default=False)
    
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    
    cliente = relationship("Cliente", back_populates="pedidos")
    
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")