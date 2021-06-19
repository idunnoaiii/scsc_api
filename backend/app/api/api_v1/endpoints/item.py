from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.crud_item import item as ItemCRUD
from app.models import item as ItemModel
from app.schemas import item as ItemSchema
from typing import List


router = APIRouter()

@router.get("/", response_model=List[ItemSchema.Item])
def read_item(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    items = ItemCRUD.get_multi(db, skip=skip, limit=limit)
    return items