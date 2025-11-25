from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ItemPedido(Base):
    __tablename__ = "itens_pedidos"

    id = Column(Integer, primary_key=True, index=True)
    
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    item_cardapio_id = Column(Integer, ForeignKey("itens_cardapio.id"), nullable=False)
    
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario_registrado = Column(Float, nullable=False)
    
    observacoes = Column(String, nullable=True) 

    pedido = relationship("Pedido", back_populates="itens")
    item_cardapio = relationship("ItemCardapio")