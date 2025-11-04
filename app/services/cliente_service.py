from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from fastapi import HTTPException

def listar_clientes(db: Session):
    return db.query(Cliente).all()

def buscar_cliente(db: Session, cliente_id: int):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

def criar_cliente (db: Session, nome: str, email: str, vip: bool = False):
    novo_cliente = Cliente(name=nome, email=email, vip=vip)
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

def atualizar_cliente(db: Session, cliente_id: int, name: str | None = None, vip: bool | None = None):
    cliente = buscar_cliente(db, cliente_id)
    if name is not None:
        cliente.name = name
    if vip is not None:
        cliente.vip = vip
    db.commit()
    db.refresh(cliente)
    return cliente

def deletar_cliente(db: Session, cliente_id: int):
    cliente = buscar_cliente(db, cliente_id)
    db.delete(cliente)
    db.commit()
    return {"mensagem": "Cliente removido"}