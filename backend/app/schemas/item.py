from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import DateTime, Float, sql
from sqlalchemy.sql.schema import Column


# Shared properties
class ItemBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float]
    expired_date: Optional[datetime]
    image_url: Optional[str]
    quantity: Optional[int] 
    category_id: Optional[int] = None
    stock: Optional[bool] = True

# Properties to receive on item creation
class ItemCreate(ItemBase):
    created_date: datetime
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

