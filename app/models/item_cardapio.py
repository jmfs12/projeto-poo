from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ItemCardapio(Base):
    __tablename__ = "itens_cardapio"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco_base = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "item",
        "polymorphic_on": tipo,
    }

    def calcular_preco_final(self):
        return self.preco_base


class PratoEntrada(ItemCardapio):
    __mapper_args__ = {"polymorphic_identity": "entrada"}

    def calcular_preco_final(self):
        return self.preco_base * 1.05


class PratoPrincipal(ItemCardapio):
    __mapper_args__ = {"polymorphic_identity": "principal"}

    def calcular_preco_final(self):
        return self.preco_base * 1.10


class Sobremesa(ItemCardapio):
    __mapper_args__ = {"polymorphic_identity": "sobremesa"}

    def calcular_preco_final(self):
        return self.preco_base * 0.95
