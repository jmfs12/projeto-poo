from fastapi import FastAPI
from app.database import Base, engine
from app.router import cliente_router, item_cardapio_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(cliente_router.router)
app.include_router(item_cardapio_router.router)

@app.get("/")
def root():
    return {"message": "API is running"}