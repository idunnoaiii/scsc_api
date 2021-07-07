from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import DateTime, Float, sql
from sqlalchemy.sql import schema
from app.schemas.customer import Customer
from .user import UserInDBBase


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


class OrderItem(OrderItemBase):

    class Config:
        orm_mode = True



class OrderItemInDB(OrderItemInDBBase):
    pass


# ---- Order section ---------------------------


# Shared properties
class OrderBase(BaseModel):
    customer_id: Optional[int] = None
    code: Optional[int]
    user_id: Optional[int]
    subtotal: Optional[int]
    total: Optional[int]
    discount: Optional[int]
    paid: Optional[int]
    change: Optional[int]
    order_items: Optional[List[OrderItemBase]] # fix the pkey error


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
class Order(OrderBase):
    order_items: Optional[List[OrderItem]] # fix the pkey error

    class Config:
        orm_mode = True


class OrderTrans(OrderBase):
    created_date: datetime
    cutomer: Optional[Customer]
    user: Optional[UserInDBBase]
    order_items: Optional[List[OrderItem]] # fix the pkey error

    class Config:
        orm_mode = True


# Properties properties stored in DB
class OrderInDB(OrderInDBBase):
    pass





