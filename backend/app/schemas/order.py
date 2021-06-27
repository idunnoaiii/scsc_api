from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import DateTime, Float, sql
from sqlalchemy.sql import schema


# ---- OrderItem section ---------------------------

class OrderItemBase(BaseModel):
    order_id: Optional[int]
    item_id: Optional[int]
    price: Optional[int]
    quantity: Optional[int]
    item_name: str

class OrderItemCreate(OrderItemBase):
    pass


class OrderItemInDBBase(OrderItemBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


class OrderItem(OrderItemInDBBase):
    pass


class OrderItemInDB(OrderItemInDBBase):
    pass


# ---- Order section ---------------------------


# Shared properties
class OrderBase(BaseModel):
    customer_id: Optional[int] = None
    user_id: Optional[int]
    status: Optional[bool]
    tax: Optional[int]
    subtotal: Optional[int]
    paid: Optional[int]
    change: Optional[int]
    order_items: Optional[List[OrderItemBase]]


# Properties to receive on item creation
class OrderCreate(OrderBase):
    created_date: datetime
    pass


#roperties to receive on item update
class OrderUpdate(OrderBase):
    updated_date: datetime 
    pass


# Properties shared by models stored in DB
class OrderInDBBase(OrderBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


# Properties to return to client
class Order(OrderInDBBase):
    order_items: Optional[List[OrderItem]]
    pass


# Properties properties stored in DB
class OrderInDB(OrderInDBBase):
    pass





