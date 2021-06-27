from typing import List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app.schemas import Category, CategoryCreate
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