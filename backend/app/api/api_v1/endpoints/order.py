import json
from app.schemas.order import OrderTrans
import fastapi
from fastapi.param_functions import Body
from typing import List
from fastapi import APIRouter, Depends, Query, Header, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Integer
from app.api.deps import get_db

from app.repositories import order_repo, user_repo
from app.schemas import Order, OrderCreate

import datetime
from app.api.deps import redis_connect

redis_client = redis_connect()

router = APIRouter()


@router.get("/all", response_model=List[Order])
def read_item(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    orders = order_repo.get_multi(db, skip=skip, limit=limit)
    return orders


@router.post("/", response_model=Order)
def create(
    db: Session = Depends(get_db),
    x_token: str = Header(...),
    create_obj: Order = Body(...)
):
    try:
        user = user_repo.get_by_userid(db, id=create_obj.user_id)
        user_key_token = redis_client.execute_command(
            "JSON.GET", "users", f".{user.username}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
    else:
        if user_key_token is None or user_key_token == "" or json.loads(user_key_token) != x_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

        res = order_repo.create_v2(db, obj_in=create_obj)
        if res.id > 0:
            user_repo.subtract_balance(
                db, user_id=res.user_id, amount=create_obj.total)


@router.patch("/{order_code}")
def checkout_onhold(
    db: Session = Depends(get_db),
    order_code: int = 0
):
    if order_code == 0:
        return



@router.get("/filter", response_model=List[OrderTrans])
def get_order_by_daterange(
    db: Session = Depends(get_db),
    startDate: datetime.datetime = Query(...),
    endDate: datetime.datetime = Query(...)
):
    return order_repo.filter_by_daterange(db, startDate=startDate, endDate=endDate)
