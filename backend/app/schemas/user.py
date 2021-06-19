from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Boolean, String
from .item import Item


class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: str = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserCreate(UserBase):
    email: str
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str