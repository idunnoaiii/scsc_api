from typing import List
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.repositories.base import RepoBase
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderUpdate


class OrderRepo(RepoBase[Order, OrderCreate, OrderUpdate]):
    
    def create_v2(self, db: Session, *, obj_in: OrderCreate) -> Order:

        obj_dict = jsonable_encoder(obj_in)
        obj_in_data = dict((k, [OrderItem(**x) for x in v]) if k == 'order_items' else (k, v) for k, v in obj_dict.items())
        order_db = Order(**obj_in_data)  # type: ignore
        db.add(order_db)
        db.commit()
        db.refresh(order_db)
        return order_db



order = OrderRepo(Order)