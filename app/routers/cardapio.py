from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.cardapio_service import CardapioService

router = APIRouter(prefix="/cardapio", tags=["Cardápio"])

def get_cardapio_service(db: Session = Depends(get_db)):
    return CardapioService(db)

def _item_dict(service: CardapioService, item):
    return {
        "id": item.id,
        "nome": item.nome,
        "tipo": item.tipo,
        "preco_base": item.preco_base,
        "preco_final": service.calcular_preco_final(item),
    }

@router.post("/")
def criar_item(
    nome: str, 
    preco_base: float, 
    tipo: str, 
    service: CardapioService = Depends(get_cardapio_service)
):
    item = service.criar_item(nome, preco_base, tipo)
    return _item_dict(service, item)

@router.get("/")
def listar_itens(service: CardapioService = Depends(get_cardapio_service)):
    itens = service.listar_itens()
    return [_item_dict(service, i) for i in itens]

@router.get("/{item_id}")
def obter_item(item_id: int, service: CardapioService = Depends(get_cardapio_service)):
    item = service.obter_item(item_id)
    return _item_dict(service, item)

@router.put("/{item_id}")
def atualizar_item(
    item_id: int, 
    nome: str = None, 
    preco_base: float = None, 
    service: CardapioService = Depends(get_cardapio_service)
):
    item = service.atualizar_item(item_id, nome, preco_base)
    return _item_dict(service, item)

@router.delete("/{item_id}")
def remover_item(item_id: int, service: CardapioService = Depends(get_cardapio_service)):
    return service.remover_item(item_id)