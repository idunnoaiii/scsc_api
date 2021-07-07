from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app.schemas import Discount, DiscountCreate, DiscountUpdate
from app.api.deps import get_db
from app.repositories import discount_repo

router = APIRouter()


@router.get("/", response_model=List[Discount])
def read_customer(
    db: Session = Depends(get_db)
):
    return discount_repo.get_multi(db, limit=None, skip=None)


@router.post("/", response_model=Discount)
def create(
    db: Session = Depends(get_db),
    create_obj: DiscountCreate = Body(...)
):
    return discount_repo.create(db, obj_in=create_obj)



@router.put("/", response_model=Discount)
def create(
    db: Session = Depends(get_db),
    update_obj: DiscountUpdate = Body(...)
):
    db_obj = discount_repo.get(db, id=update_obj.id)
    if db_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return discount_repo.update(db, db_obj=db_obj, obj_in=update_obj)


@router.delete("/")
def delete(
    db: Session = Depends(get_db),
    id: int = Path(...)
):
    if id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    discount_repo.in_active(db, id=id)
    return True


@router.get("/calculate/{amount}")
def calculate(
    db: Session = Depends(get_db),
    amount: int = Path(...)
):
    list_discounts =  discount_repo.get_all(db)
    if list_discounts != []:
        for discount in list_discounts:
            if amount >= discount.threshold:
                return {
                    "threshold": discount.threshold,
                    "type": discount.type,
                    "value": discount.value
                }
    
    return  {
        "threshold": 0,
        "type": 0,
        "value": 0
    }

