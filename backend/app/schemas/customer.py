from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import DateTime, Float, sql



class CustomerBase(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerInDBBase(CustomerBase):
    id: int
    class Config:
        orm_mode = True


class Customer(CustomerBase):

    class Config: 
        orm_mode = True


class CustomerInDB(CustomerInDBBase):
    pass
