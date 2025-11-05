from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import cliente_service

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/")
def listar_clientes(db: Session = Depends(get_db)):
    return cliente_service.listar_clientes(db)

@router.get("/{cliente_id}")
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return cliente_service.buscar_cliente(db, cliente_id)

@router.post("/")
def criar_cliente(name: str, email: str, vip: bool = False, db: Session = Depends(get_db)):
    return cliente_service.criar_cliente(db, name, email, vip)

@router.put("/{cliente_id}")
def atualizar_cliente(cliente_id: int, name: str | None = None, vip: bool | None = None, db: Session = Depends(get_db)):
    return cliente_service.atualizar_cliente(db, cliente_id, name, vip)

@router.delete("/{cliente_id}")
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return cliente_service.deletar_cliente(db, cliente_id)