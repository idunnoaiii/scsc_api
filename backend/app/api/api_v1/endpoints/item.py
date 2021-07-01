from fastapi import APIRouter, Depends, Body, Request, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import File, Form
from sqlalchemy.orm import Session
from starlette.datastructures import FormData
from app.api import deps
from app.repositories import item_repo
from app.schemas import Item, ItemCreate
from typing import List
import base64
import json
from app.ai_utils import predict
import shutil

router = APIRouter()

@router.get("/all", response_model=List[Item])
def read_item(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    items = item_repo.get_multi(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=Item)
def create_item(
    db: Session = Depends(deps.get_db),
    item: ItemCreate = Body(...)
):
    return item_repo.create(db, obj_in=item)


# - Create item with form post  
# - data: a json string of Item
# - image: image of item
@router.post("/create")
def create_item_form(
    db: Session = Depends(deps.get_db),
    data: str = Form(...),
    image: UploadFile = File(...),

):
    #this stimulate the process upload image to some cloud storage and get URL
    with open("image/"+image.filename, "wb") as file:
        shutil.copyfileobj(image.file, file)
    
    item_json = json.loads(data)
    item_json["image_url"] = image.filename
    item_create_sch = ItemCreate(**item_json)
    return item_repo.create(db, obj_in=item_create_sch)



@router.post("/scan/")
async def scan_item(
    db: Session = Depends(deps.get_db),
    req: Request = None
):
    img_base64 = await req.body()
    class_ids = predict(img_base64[22:])

    if class_ids != [] and class_ids[0] == -1:
        return [-1]

    elif class_ids != []:
        items = item_repo.get_multi_by_list_id(db, listId=class_ids)
        return items

    return []


#test the upload image
@router.post("/test")
async def create_item_form(
    db: Session = Depends(deps.get_db),
    dataText: str = Form(...),
    image: UploadFile = File(...)
):
    with open(image.filename, 'wb') as f:
        shutil.copyfileobj(image.file, f)

    return {
        "dataText": dataText,
        "imageURL": image.filename
    }