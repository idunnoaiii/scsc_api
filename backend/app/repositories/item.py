from typing import Dict, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.repositories.base import RepoBase
from app.models import ItemModel, CategoryModel
from app.schemas import ItemCreate, ItemUpdate, ItemToCache


class ItemRepo(RepoBase[ItemModel, ItemCreate, ItemUpdate]): 
    def create_with_owner(
        self, db: Session, *, obj_in: dict, owner_id: int
    ) -> ItemModel:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[ItemModel]:
        
        return (
            db.query(self.model)
            .filter(ItemModel.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


    def create(
        self,
        db: Session,
        *,
        obj_dict: Dict
    ) -> ItemModel:

        temp_cate = obj_dict["categories"] if "categories" in obj_dict else []
        if temp_cate != []: 
            del obj_dict["categories"] 
        obj_db = ItemModel(**obj_dict)

        if temp_cate != []:
            cates = db.query(CategoryModel).filter(CategoryModel.id.in_(temp_cate)).all()
            obj_db.categories = cates


        db.add(obj_db)
        db.commit()
        db.refresh(obj_db)
        return obj_db



    def update(
        self,
        db: Session,
        *,
        obj_dict: Dict
    ) -> ItemModel:

        obj_db = db.query(ItemModel).get(obj_dict["id"])
        obj_db_data = jsonable_encoder(obj_db)

        #update field
        for field in obj_db_data:
            if field in obj_dict:
                setattr(obj_db, field, obj_dict[field])

        #update child
        # new_cate_ids = [j for j in obj_dict["categories"] if j not in [cate.id for cate in obj_db.categories]]

        if obj_dict["categories"] != []:
            cates = db.query(CategoryModel).filter(CategoryModel.id.in_(obj_dict["categories"])).all()
            obj_db.categories = cates

        db.add(obj_db)
        db.commit()
        db.refresh(obj_db)
        return obj_db


    def search(
        self,
        db: Session,
        *,
        searchValue: str,
        categories: List[int]
    ):
        ret = []
        items = set()
        searchValue = searchValue.strip().lower() if searchValue is not None else ""
        if categories != []:
            cates = db.query(CategoryModel).filter(
                    CategoryModel.id.in_(categories)
            ).all()

            for cat in cates:
                for i in cat.items:
                    items.add(i)

            ret = [i for i in items if searchValue == "" or (i.name.lower().find(searchValue.lower()) != -1) or (i.slug.lower().find(searchValue.lower()) != -1)]
            return ret

        return db.query(ItemModel).filter(
            or_(ItemModel.name.ilike("%"+searchValue+"%"),
            ItemModel.slug.ilike("%"+searchValue+"%"))
            ).filter(ItemModel.is_active == True).all()


    def fetch_by_ids(
        self, db: Session, *, listId: List[int]
    ):
        return db.query(ItemModel).filter(self.model.id.in_(listId)).all()

    # def update(
    #     self,
    #     db: Session,
    #     *,
    #     db_obj: ItemModel,
    #     obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    # ) -> ModelType:
    #     obj_data = jsonable_encoder(db_obj)
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     for field in obj_data:
    #         if field in update_data:
    #             setattr(db_obj, field, update_data[field])
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj 

    def get_item_to_cache(self, db: Session) -> List[ItemToCache]:
        return db.query(ItemModel).filter(self.model.is_active == True).all()

item = ItemRepo(ItemModel)