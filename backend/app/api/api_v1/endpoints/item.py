from fastapi import APIRouter, Depends, Body, Request
from fastapi.datastructures import UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import File
from pydantic.main import BaseModel
from pydantic.utils import import_string
from sqlalchemy.engine import base
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.crud_item import item as ItemCRUD
from app.models import item as ItemModel
from app.schemas import item as ItemSchema
from typing import Any, List
import base64
import json
from app.ai_utils.predict import predict

router = APIRouter()

@router.get("/all", response_model=List[ItemSchema.Item])
def read_item(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    items = ItemCRUD.get_multi(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=ItemSchema.Item)
def create_item(
    db: Session = Depends(deps.get_db),
    item: ItemSchema.ItemCreate = Body(...)
):
    return ItemCRUD.create(db, obj_in=item)


@router.post("/scan/", )
async def scan_item(
    db: Session = Depends(deps.get_db),
    req: Request = None
):
    img_base64 = await req.body()
    class_ids = predict(img_base64[22:])

    if class_ids != [] and class_ids[0] == -1:
        return [-1]

    elif class_ids != []:
        items = ItemCRUD.get_multi_by_list_id(db, listId=class_ids)
        return items

    return []


