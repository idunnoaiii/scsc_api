from fastapi.param_functions import Body
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps

from app.crud.crud_order import order as CRUDOrder
from app.schemas import order as OrderSchema

router = APIRouter()


@router.get("/all", response_model=List[OrderSchema.Order])
def read_item(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    orders = CRUDOrder.get_multi(db, skip=skip, limit=limit)
    return orders


@router.post("/", response_model=OrderSchema.Order)
def create(
    db: Session = Depends(deps.get_db),
    create_obj: OrderSchema.OrderCreate = Body(...)
):
    return CRUDOrder.create_v2(db, obj_in=create_obj)