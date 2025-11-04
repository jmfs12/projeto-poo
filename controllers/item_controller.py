
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.item_model import ItemCreate, ItemResponse
from services.item_service import ItemService
from database.database import get_db

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return ItemService.create_item(db, item)

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = ItemService.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item

@router.get("/", response_model=List[ItemResponse])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ItemService.get_items(db, skip, limit)

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    updated_item = ItemService.update_item(db, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return updated_item

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    if not ItemService.delete_item(db, item_id):
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"message": "Item deletado com sucesso"}