from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from fastapi import HTTPException

class ClienteService:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.query(Cliente).all()

    def buscar(self, cliente_id: int):
        cliente = self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return cliente

    def criar(self, nome: str, email: str, vip: bool = False):
        novo_cliente = Cliente(name=nome, email=email, vip=vip)
        self.db.add(novo_cliente)
        self.db.commit()
        self.db.refresh(novo_cliente)
        return novo_cliente

    def atualizar(self, cliente_id: int, name: str | None = None, vip: bool | None = None):
        cliente = self.buscar(cliente_id)
        if name is not None:
            cliente.name = name
        if vip is not None:
            cliente.vip = vip
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def deletar(self, cliente_id: int):
        cliente = self.buscar(cliente_id)
        self.db.delete(cliente)
        self.db.commit()
        return {"mensagem": "Cliente removido"}
