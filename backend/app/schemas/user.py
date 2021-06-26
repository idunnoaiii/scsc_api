from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Boolean, String


class UserBase(BaseModel):
    full_name: Optional[str] = None
    username: str = None
    is_admin: Optional[bool] = True


class UserCreate(UserBase):
    username: str
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