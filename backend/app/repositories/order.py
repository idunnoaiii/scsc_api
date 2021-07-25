from datetime import datetime
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.repositories.base import RepoBase
from app.models.order import Order, OrderItem
from app.models import ItemModel
from app.schemas.order import OrderCreate, OrderUpdate


class OrderRepo(RepoBase[Order, OrderCreate, OrderUpdate]):
    
    def create_v2(self, db: Session, *, obj_in: OrderCreate) -> Order:

        obj_dict = jsonable_encoder(obj_in)
        obj_in_data = dict((k, [OrderItem(**x) for x in v]) if k == 'order_items' else (k, v) for k, v in obj_dict.items())
        order_db = Order(**obj_in_data)  # type: ignore

        for item in obj_in_data["order_items"]:
            item_db = db.query(ItemModel).get(item.item_id)
            # item_db.quantity = item_db.quantity - item.quantity
            # if item_db.quantity <= 0:
            #     item_db.quantity = 0

        db.add(order_db)
        db.commit()
        db.refresh(order_db)
        return order_db


    def filter_by_daterange(self, db: Session, *, startDate: datetime, endDate: datetime) -> List[Order]:
        return db.query(Order).filter(
            and_(

                Order.is_active == True,
                Order.created_date >= startDate,
                Order.created_date <= endDate
            )
        ).order_by(Order.updated_date.desc()).all()



order = OrderRepo(Order)