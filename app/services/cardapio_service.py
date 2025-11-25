from sqlalchemy.orm import Session
from app.models.item_cardapio import ItemCardapio, PratoEntrada, PratoPrincipal, Sobremesa
from fastapi import HTTPException

class CardapioService:
    def __init__(self, db: Session):
        self.db = db

    def criar_item(self, nome: str, preco_base: float, tipo: str) -> ItemCardapio:
        tipos_map = {
            "entrada": PratoEntrada,
            "principal": PratoPrincipal,
            "sobremesa": Sobremesa,
            "item": ItemCardapio
        }

        cls = tipos_map.get(tipo.lower())
        if not cls:
            raise HTTPException(status_code=400, detail=f"Tipo de item inválido: {tipo}")

        novo_item = cls(nome=nome, preco_base=preco_base, tipo=tipo.lower())
        
        self.db.add(novo_item)
        self.db.commit()
        self.db.refresh(novo_item)
        return novo_item

    def listar_itens(self):
        return self.db.query(ItemCardapio).all()

    def obter_item(self, item_id: int):
        item = self.db.query(ItemCardapio).filter(ItemCardapio.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item do cardápio não encontrado.")
        return item
    
    def atualizar_item(self, item_id: int, nome: str = None, preco_base: float = None):
        item = self.obter_item(item_id)
        if nome:
            item.nome = nome
        if preco_base:
            item.preco_base = preco_base
        self.db.commit()
        self.db.refresh(item)
        return item

    def remover_item(self, item_id: int):
        item = self.obter_item(item_id)
        self.db.delete(item)
        self.db.commit()
        return {"mensagem": "Item removido do cardápio"}
    
    def calcular_preco_final(self, item: ItemCardapio) -> float:
        return item.calcular_preco_final()