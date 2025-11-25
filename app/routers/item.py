from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.item_pedido_service import ItemPedidoService

router = APIRouter(prefix="/itens-pedido", tags=["Itens do Pedido"])

def get_item_pedido_service(db: Session = Depends(get_db)):
    return ItemPedidoService(db)

@router.post("/")
def adicionar_item_avulso(
    pedido_id: int,
    item_cardapio_id: int,
    quantidade: int = 1,
    observacoes: str = None,
    service: ItemPedidoService = Depends(get_item_pedido_service)
):

    novo_item = service.adicionar_item_ao_pedido(pedido_id, item_cardapio_id, quantidade, observacoes)
    return {
        "mensagem": "Item adicionado ao pedido",
        "item_id": novo_item.id,
        "preco_registrado": novo_item.preco_unitario_registrado
    }

@router.delete("/{item_pedido_id}")
def remover_item_do_pedido(
    item_pedido_id: int, 
    service: ItemPedidoService = Depends(get_item_pedido_service)
):
    service.remover_item_do_pedido(item_pedido_id)
    return {"mensagem": "Item removido do pedido"}