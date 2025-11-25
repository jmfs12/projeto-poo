from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.cliente_service import ClienteService 

router = APIRouter(prefix="/clientes", tags=["Clientes"])

def get_cliente_service(db: Session = Depends(get_db)):
    return ClienteService(db)

@router.get("/")
def listar_clientes(service: ClienteService = Depends(get_cliente_service)):
    return service.listar_clientes()

@router.get("/{cliente_id}")
def buscar_cliente(cliente_id: int, service: ClienteService = Depends(get_cliente_service)):
    return service.buscar_cliente(cliente_id)

@router.post("/")
def criar_cliente(
    name: str, 
    email: str, 
    vip: bool = False, 
    service: ClienteService = Depends(get_cliente_service)
):
    return service.criar_cliente(name, email, vip)

@router.put("/{cliente_id}")
def atualizar_cliente(
    cliente_id: int, 
    name: str | None = None, 
    vip: bool | None = None, 
    service: ClienteService = Depends(get_cliente_service)
):
    return service.atualizar_cliente(cliente_id, name, vip)

@router.delete("/{cliente_id}")
def deletar_cliente(cliente_id: int, service: ClienteService = Depends(get_cliente_service)):
    return service.deletar_cliente(cliente_id)