from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.item_cardapio_service import CardapioService

router = APIRouter(prefix="/cardapio", tags=["Cardápio"])

@router.post("/")
def criar_item(nome: str, preco_base: float, tipo: str, db: Session = Depends(get_db)):
    service = CardapioService(db)
    try:
        item = service.criar_item(nome, preco_base, tipo)
        return _item_dict(service, item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def listar_itens(db: Session = Depends(get_db)):
    service = CardapioService(db)
    itens = service.listar_itens()
    return [_item_dict(service, i) for i in itens]


@router.get("/{item_id}")
def obter_item(item_id: int, db: Session = Depends(get_db)):
    service = CardapioService(db)
    try:
        item = service.obter_item(item_id)
        return _item_dict(service, item)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{item_id}")
def atualizar_item(item_id: int, nome: str = None, preco_base: float = None, db: Session = Depends(get_db)):
    service = CardapioService(db)
    try:
        item = service.atualizar_item(item_id, nome, preco_base)
        return _item_dict(service, item)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{item_id}")
def remover_item(item_id: int, db: Session = Depends(get_db)):
    service = CardapioService(db)
    try:
        item = service.remover_item(item_id)
        return {"mensagem": f"Item '{item.nome}' removido com sucesso."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


def _item_dict(service: CardapioService, item):
    return {
        "id": item.id,
        "nome": item.nome,
        "tipo": item.tipo,
        "preco_base": item.preco_base,
        "preco_final": service.calcular_preco_final(item),
    }
