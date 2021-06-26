from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import DateTime, Float, sql



class CategoryBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    created_date: datetime
    pass

class CategoryUpdate(CategoryBase):
    updated_date: datetime
    pass



class CategoryInDBBase(CategoryBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


class Category(CategoryBase):
    pass


class CategoryInDB(CategoryInDBBase):
    pass
