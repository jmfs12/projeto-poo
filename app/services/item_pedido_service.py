from sqlalchemy.orm import Session
from app.models.item_pedido import ItemPedido
from app.models.item_cardapio import ItemCardapio
from fastapi import HTTPException

class ItemPedidoService:
    def __init__(self, db: Session):
        self.db = db

    def adicionar_item_ao_pedido(self, pedido_id: int, item_cardapio_id: int, quantidade: int = 1, observacoes: str = None):
        item_cardapio = self.db.query(ItemCardapio).filter(ItemCardapio.id == item_cardapio_id).first()
        if not item_cardapio:
            raise HTTPException(status_code=404, detail=f"Item de cardápio {item_cardapio_id} não encontrado")

        preco_calculado = item_cardapio.calcular_preco_final()

        novo_item_pedido = ItemPedido(
            pedido_id=pedido_id,
            item_cardapio_id=item_cardapio_id,
            quantidade=quantidade,
            preco_unitario_registrado=preco_calculado,
            observacoes=observacoes
        )

        self.db.add(novo_item_pedido)
        self.db.commit()
        self.db.refresh(novo_item_pedido)
        return novo_item_pedido

    def remover_item_do_pedido(self, item_pedido_id: int):
        item_pedido = self.db.query(ItemPedido).filter(ItemPedido.id == item_pedido_id).first()
        if item_pedido:
            self.db.delete(item_pedido)
            self.db.commit()