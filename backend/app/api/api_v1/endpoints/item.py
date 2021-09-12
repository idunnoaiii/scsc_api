from fastapi import APIRouter, Depends, Body, Request, Form, UploadFile, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import File, Form, Path
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import true
from starlette.datastructures import FormData
from app.api import deps
from app.repositories import item_repo
from app.schemas import Item, ItemCreate, User, ItemCheckoutModel
from app.models import CategoryModel
from typing import List, Optional
import base64
import json
from app.ai_utils import predict_2, predict
import shutil
import time
from slugify import slugify
import io

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
    
    # item_categories = item_json["categories"]

    # item_json["categories"] = [{"id": v} for v in item_categories]

    item_json["slug"] = slugify(item_json["name"], separator=" ")

    # del item_json["categories"]
    # item_create_sch = ItemCreate(**item_json)
    created = item_repo.create(db, obj_dict=item_json)


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
    
    item_json["slug"] = slugify(item_json["name"], separator=" ")

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
    start = time.time()
    img_base64 = await req.body()
    class_ids, positions = predict_2(img_base64[22:])
    if class_ids is None:
        return None

    if class_ids != []:
        class_id_count = {i:class_ids.count(i) for i in class_ids}
        items = item_repo.get_multi_by_list_id(db, listId=class_ids)
        for item in items:
            if item.id in class_id_count.keys():
                item.quantity = class_id_count[item.id]

        end = time.time()
        print(end - start)
        return {
            "items": items,
            "positions": positions 
        }

    return None


@router.post("/fetch/", response_model= List[ItemCheckoutModel])
async def fetch_items(
    db: Session = Depends(deps.get_db),
    class_ids: List[int] = Body(None)
):
    start = time.time()
    if class_ids is None or class_ids == []:
        return None

    class_id_count = {i:class_ids.count(i) for i in class_ids}
    items = item_repo.fetch_by_ids(db, listId=class_ids)
    for item in items:
        if item.id in class_id_count.keys():
            item.quantity = class_id_count[item.id]

    end = time.time()
    print(end - start)
    return items




@router.post("/upload-image/")
async def upload_image(
    bucket = Depends(deps.get_firebase_bucket),
    body: str = Body(None)

):

    req_body = json.loads(body)

    if req_body["image"] == "" and req_body["positions"] == "":
        return
    
    positions = req_body["positions"]
    image = base64.b64decode(req_body["image"][22:]); 

    file_name = int(time.time()*1000)

    # with open(f'upload/{file_name}.txt', 'w') as file:
    #     for v in positions:
    #         file.write(f"{v[0]} {v[1]} {v[2]} {v[3]} {v[4]}\n")

    # with open(f'upload/{file_name}.txt', 'rb') as file:
    #     blob = bucket.blob(f"data_train/{file_name}.txt")
    #     blob.upload_from_file(file, content_type="text/plain")
    #     blob.make_public()
    #     print(blob.public_url)
    text_position = ""
    for v in positions:
        text_position = text_position  + f"{v[0]} {v[1]} {v[2]} {v[3]} {v[4]}\n"

    print(text_position)

    blob_text = bucket.blob(f"data_train/{file_name}.txt")
    blob_text.upload_from_file(io.StringIO(text_position), content_type="text/plain")
    blob_text.make_public()
    print(blob_text.public_url)
    
    blob_image = bucket.blob(f"data_train/{file_name}.png")
    blob_image.upload_from_file(io.BytesIO(image), content_type="image/png")
    blob_image.make_public()
    print(blob_image.public_url)



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
    