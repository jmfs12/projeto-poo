from sqlalchemy.orm import Session
from app.models.pedido import Pedido
from app.models.cliente import Cliente
from app.services.item_pedido_service import ItemPedidoService # Importando o novo serviço
from fastapi import HTTPException

class PedidoService:
    def __init__(self, db: Session):
        self.db = db
        self.item_pedido_service = ItemPedidoService(db)

    def obter_pedido(self, pedido_id: int):
        pedido = self.db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")
        return pedido

    def calcular_total_pedido(self, pedido_id: int) -> float:
        pedido = self.obter_pedido(pedido_id)
        total = 0.0
        
        for item_pedido in pedido.itens:
            total += item_pedido.preco_unitario_registrado * item_pedido.quantidade
            
        return total
    
    def criar_pedido(self, cliente_id: int, itens_entrada: list[dict], descricao: str = None):
        cliente = self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        novo_pedido = Pedido(descricao=descricao, cliente_id=cliente_id)
        self.db.add(novo_pedido)
        self.db.commit()
        self.db.refresh(novo_pedido)

        try:
            for item_data in itens_entrada:
                self.item_pedido_service.adicionar_item_ao_pedido(
                    pedido_id=novo_pedido.id,
                    item_cardapio_id=item_data['item_id'],
                    quantidade=item_data.get('quantidade', 1),
                    observacoes=item_data.get('observacoes')
                )
        except Exception as e:
            self.db.delete(novo_pedido)
            self.db.commit()
            raise e

        self.db.refresh(novo_pedido)
        return novo_pedido

    def atualizar_status_entrega(self, pedido_id: int, entregue: bool):
        pedido = self.obter_pedido(pedido_id)
        pedido.entregue = entregue
        self.db.commit()
        self.db.refresh(pedido)
        return pedido
    
    def deletar_pedido(self, pedido_id: int):
        pedido = self.obter_pedido(pedido_id)
        self.db.delete(pedido)
        self.db.commit()
        return {"mensagem": "Pedido removido"}