from fastapi.param_functions import Body
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps

from app.repositories import order_repo
from app.schemas import Order, OrderCreate

router = APIRouter()


@router.get("/all", response_model=List[Order])
def read_item(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    orders = order_repo.get_multi(db, skip=skip, limit=limit)
    return orders


@router.post("/", response_model=Order)
def create(
    db: Session = Depends(deps.get_db),
    create_obj: OrderCreate = Body(...)
):
    return order_repo.create_v2(db, obj_in=create_obj)