from fastapi import APIRouter, Depends, Body, Request, Form, UploadFile, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import File, Form, Path
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import true
from starlette.datastructures import FormData
from app.api import deps
from app.repositories import item_repo
from app.schemas import Item, ItemCreate, User
from app.models import CategoryModel
from typing import List, Optional
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
    ret = []
    items = item_repo.get_multi(db, skip=skip, limit=limit)
    for item in items:
        itemDic = item.__dict__
        cates = [cate.__dict__["id"] for cate in item.categories]
        itemDic["categories"] = cates
        ret.append(itemDic)

    return ret


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
    bucket = Depends(deps.get_firebase_bucket),
    data: str = Form(...),
    image: UploadFile = File(None),

):
    item_json = json.loads(data)

    if image is not None:
        # item_json["image_url"] = image.filename
        try:
            blob = bucket.blob(f"image/{image.filename}")
            blob.upload_from_file(image.file)
            blob.make_public()
        except:
            pass
        else:
            item_json["image_url"] = blob.public_url
        #this stimulate the process upload image to some cloud storage and get URL
        # with open("image/"+image.filename, "wb") as file:
        #     shutil.copyfileobj(image.file, file)
    
    item_categories = item_json["categories"]

    item_json["categories"] = [{"id": v} for v in item_categories]

    # del item_json["categories"]
    item_create_sch = ItemCreate(**item_json)
    created = item_repo.create(db, obj_in=item_create_sch)


@router.put("/update")
def update_item(
    db: Session = Depends(deps.get_db),
    bucket = Depends(deps.get_firebase_bucket),
    data: str = Form(...),
    image: UploadFile = File(None)
):
    item_json = json.loads(data)

    if image is not None:
        # item_json["image_url"] = image.filename
        try:
            blob = bucket.blob(f"image/{image.filename}")
            blob.upload_from_file(image.file)
            blob.make_public()
        except:
            pass
        else:
            item_json["image_url"] = blob.public_url

        #this stimulate the process upload image to some cloud storage and get URL
        # with open("image/"+image.filename, "wb") as file:
        #     shutil.copyfileobj(image.file, file)

    item_in_db = item_repo.get(db, id=item_json["id"])

    if item_in_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    item_repo.update(db,  obj_dict=item_json)

    if image is not None:
        pass


    return True

    


# for scanning function
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
        class_id_count = {i:class_ids.count(i) for i in class_ids}
        items = item_repo.get_multi_by_list_id(db, listId=class_ids)
        print(class_id_count)
        for item in items:
            if item.id in class_id_count.keys():
                item.quantity = class_id_count[item.id]

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


@router.delete("/{id}")
def delete(
    db: Session = Depends(deps.get_db),
    id: int = Path(...)
):
    if id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    item_repo.in_active(db, id=id)
    return True



@router.post("/search")
def search_item(
    db: Session = Depends(deps.get_db),
    searchValue: str = Body(None),
    categories_selected: List[int] = Body(...)
):
    return item_repo.search(db, searchValue= searchValue,categories= categories_selected)
    