from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import DateTime, Float, sql



class CategoryBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass

class CategoryId(BaseModel):
    id: int

    class Config:
        orm_mode = True

class CategoryInDBBase(CategoryBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


class Category(CategoryBase):
    id: int
    class Config: 
        orm_mode = True



class CategoryInDB(CategoryInDBBase):
    pass
