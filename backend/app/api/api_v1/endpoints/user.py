from typing import Any, List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql.functions import mode
from app.schemas import user as schemas
from app.models import user as models
from app.crud.crud_user import user as crud
from app.db.dba import database


from app.api import deps

from app.models.user import users

router = APIRouter()


@router.get("/")
# def read_users(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100
# ):
#     users = crud.get_multi(db, skip=skip, limit=limit)
#     return users
async def read_user():
    query = models.users.select()
    users = await database.fetch_all(query)
    
    return users
    


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


# Don't do this in production!
@router.post("/", response_model=List[UserIn])
async def create_user(user: UserIn):
    a = {
        "username": "thien",
        "password": "ahihi",
        "email": "thien@gmail.com",
        "full_name": "quang thien"
    }
    return [a]