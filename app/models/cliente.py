from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True)
    vip = Column(Boolean, nullable=False, server_default="0")
