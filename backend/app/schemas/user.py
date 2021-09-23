from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Boolean, String

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    id: int
    full_name: str
    username: str
    balance: int

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Optional[str] = None


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class UserBase(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    role_id: Optional[int] = 0
    address: Optional[str] = None
    contact: Optional[str] = None
    gender: Optional[bool] = False
    balance: Optional[int] = 0


class UserCreate(UserBase):
    username: str
    password: str


class UserUpdate(UserBase):
    id: int
    password: Optional[str] = None
    pass

class UserUpdatePassword(UserBase):
    id: Optional[int] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str