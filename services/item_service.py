
from sqlalchemy.orm import Session
from models.item_model import ItemDB, ItemCreate
from typing import List, Optional

class ItemService:
    
    @staticmethod
    def create_item(db: Session, item: ItemCreate) -> ItemDB:
        db_item = ItemDB(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def get_item(db: Session, item_id: int) -> Optional[ItemDB]:
        return db.query(ItemDB).filter(ItemDB.id == item_id).first()
    
    @staticmethod
    def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[ItemDB]:
        return db.query(ItemDB).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_item(db: Session, item_id: int, item: ItemCreate) -> Optional[ItemDB]:
        db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
        if db_item:
            for key, value in item.dict().items():
                setattr(db_item, key, value)
            db.commit()
            db.refresh(db_item)
        return db_item
    
    @staticmethod
    def delete_item(db: Session, item_id: int) -> bool:
        db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
        if db_item:
            db.delete(db_item)
            db.commit()
            return True
        return False