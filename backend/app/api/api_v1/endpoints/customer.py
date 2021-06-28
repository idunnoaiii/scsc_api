from typing import List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app.schemas import Customer, CustomerCreate
from app.api.deps import get_db
from app.repositories import customer_repo

router = APIRouter()

@router.get("/", response_model=List[Customer])
def read_customer(
    db: Session = Depends(get_db)
):
    return customer_repo.get_multi(db, limit=None, skip=None)


@router.post("/", response_model=Customer)
def create(
    db: Session = Depends(get_db),
    create_obj: CustomerCreate = Body(...)
):
    return customer_repo.create(db, obj_in=create_obj)