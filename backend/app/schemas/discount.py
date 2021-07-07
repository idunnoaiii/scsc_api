from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import DateTime, Float, sql


class DiscountBase(BaseModel):
    description: Optional[str] = None
    threshold: int = 0
    type: int = 0
    value: float = 0
    is_apply: bool = False
    


class DiscountCreate(DiscountBase):
    pass


class DiscountUpdate(DiscountBase):
    id: int
    pass


class DiscountInDBBase(DiscountBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


class Discount(DiscountBase):
    id: int
    class Config: 
        orm_mode = True



class DiscountInDB(DiscountInDBBase):
    pass
