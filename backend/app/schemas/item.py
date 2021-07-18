from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel
from sqlalchemy import DateTime, Float, sql
from sqlalchemy.sql.schema import Column
from app.schemas.category import CategoryId

# Shared properties
class ItemBase(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    quantity: Optional[int] = None
    categories: Optional[List[int]] = None
    stock: Optional[bool] = False

# Properties to receive on item creation
class ItemCreate(ItemBase):
    categories: Optional[Any] = None
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    updated_date: datetime 
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass

