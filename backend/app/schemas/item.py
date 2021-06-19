from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import DateTime, Float, sql


# Shared properties
class ItemBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = 0
    expired_date: Optional[datetime]
    image_url: Optional[str]

# Properties to receive on item creation
class ItemCreate(ItemBase):
    create_date: datetime = datetime.now()
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    updated_date: datetime = datetime.now()
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