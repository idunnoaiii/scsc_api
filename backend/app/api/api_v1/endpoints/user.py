from typing import Any, List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.param_functions import Path
from fastapi.params import Param
from pydantic import BaseModel, EmailStr
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas import user as schemas
from app.models import user as UserModel
from app.repositories import user_repo
from app.db.session import engine
from app.api.deps import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    # users = crud.get_multi(db, skip=skip, limit=limit)
    # users = db.execute(UserModel.users.select()).fetchall()
    # with engine.connect() as con:
    #     users = con.execute(UserModel.users.select()).fetchall()

    # return users
    return user_repo.get_multi(db, skip=skip, limit=limit)


# @router.post("/", response_model=schemas.UserCreate)
@router.post("/")
async def create_user(
    db: Session = Depends(get_db),
    user: schemas.UserCreate = Body(...)
):
    # user_in_db = UserModel.User(**user.dict())
    user_in = user.dict()
    user_in["hashed_password"] = user_in["password"]
    del user_in["password"]
    with engine.connect() as con, con.begin() as tran:
        con.execute(UserModel.users.insert().values(**user_in))
        tran.commit()
        return True
    return False


 
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(
    db: Session = Depends(get_db),
    id: int = Path(...)
):
    if id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    user_repo.in_active(db, id=id)
    return True