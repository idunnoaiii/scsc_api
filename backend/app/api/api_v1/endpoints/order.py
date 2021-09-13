from app.schemas.order import OrderTrans
import fastapi
from fastapi.param_functions import Body
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Integer
from app.api.deps import get_db

from app.repositories import order_repo, user_repo
from app.schemas import Order, OrderCreate

import datetime

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
    create_obj: Order = Body(...)
):
    res = order_repo.create_v2(db, obj_in=create_obj)
    if res.id > 0:
        user_repo.subtract_balance(db, user_id = res.user_id, amount = create_obj.total)


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
