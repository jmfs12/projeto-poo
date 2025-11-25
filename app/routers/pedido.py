from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.pedido_service import PedidoService

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

def get_pedido_service(db: Session = Depends(get_db)):
    return PedidoService(db)

def _pedido_response(service: PedidoService, pedido):
    return {
        "id": pedido.id,
        "descricao": pedido.descricao,
        "cliente_id": pedido.cliente_id,
        "entregue": pedido.entregue,
        "total": service.calcular_total_pedido(pedido.id),
        "itens": [
            {
                "item_cardapio": item.item_cardapio.nome,
                "quantidade": item.quantidade,
                "preco_registrado": item.preco_unitario_registrado,
                "subtotal": item.preco_unitario_registrado * item.quantidade
            } 
            for item in pedido.itens
        ]
    }

@router.post("/")
def criar_pedido(
    cliente_id: int,
    descricao: str = None,
    itens: list[dict] = Body(..., example=[{"item_id": 1, "quantidade": 2}, {"item_id": 3, "quantidade": 1}]),
    service: PedidoService = Depends(get_pedido_service)
):
    novo_pedido = service.criar_pedido(cliente_id, itens, descricao)
    return _pedido_response(service, novo_pedido)

@router.get("/")
def listar_pedidos(service: PedidoService = Depends(get_pedido_service)):
    pedidos = service.listar_pedidos()
    return [_pedido_response(service, p) for p in pedidos]

@router.get("/{pedido_id}")
def obter_pedido(pedido_id: int, service: PedidoService = Depends(get_pedido_service)):
    pedido = service.obter_pedido(pedido_id)
    return _pedido_response(service, pedido)

@router.put("/{pedido_id}/entrega")
def atualizar_status_entrega(
    pedido_id: int, 
    entregue: bool, 
    service: PedidoService = Depends(get_pedido_service)
):
    pedido = service.atualizar_status_entrega(pedido_id, entregue)
    return {"id": pedido.id, "entregue": pedido.entregue, "mensagem": "Status atualizado"}

@router.delete("/{pedido_id}")
def deletar_pedido(pedido_id: int, service: PedidoService = Depends(get_pedido_service)):
    return service.deletar_pedido(pedido_id)