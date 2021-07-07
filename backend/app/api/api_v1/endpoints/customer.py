from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app.schemas import Customer, CustomerCreate, CustomerUpdate
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


@router.put("/", response_model=Customer)
def create(
    db: Session = Depends(get_db),
    update_obj: CustomerUpdate = Body(...)
):
    db_obj = customer_repo.get(db, id=update_obj.id)
    if db_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return customer_repo.update(db, db_obj=db_obj, obj_in=update_obj)


@router.delete("/")
def delete(
    db: Session = Depends(get_db),
    id: int = Path(...)
):
    if id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    customer_repo.in_active(db, id=id)
    return True