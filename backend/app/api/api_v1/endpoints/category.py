from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app.schemas import Category, CategoryCreate, CategoryUpdate
from app.api.deps import get_db
from app.repositories import category_repo

router = APIRouter()

@router.get("/", response_model=List[Category])
def read_category(
    db: Session = Depends(get_db)
):
    return category_repo.get_multi(db, limit=None, skip=None)


@router.post("/", response_model=Category)
def create(
    db: Session = Depends(get_db),
    create_obj: CategoryCreate = Body(...)
):
    return category_repo.create(db, obj_in=create_obj)



@router.put("/", response_model=Category)
def create(
    db: Session = Depends(get_db),
    update_obj: CategoryUpdate = Body(...)
):
    db_obj = category_repo.get(db, id=update_obj.id)
    if db_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return category_repo.update(db, db_obj=db_obj, obj_in=update_obj)


@router.delete("/{id}")
def delete(
    db: Session = Depends(get_db),
    id: int = Path(...)
):
    if id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    category_repo.in_active(db, id=id)
    return True