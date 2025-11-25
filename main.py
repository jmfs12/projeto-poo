from fastapi import FastAPI
from app.database import Base, engine
from app.routers import cardapio, cliente, item, pedido

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(cliente.router)
app.include_router(cardapio.router)
app.include_router(pedido.router)
app.include_router(item.router)


@app.get("/")
def root():
    return {"message": "API is running"}