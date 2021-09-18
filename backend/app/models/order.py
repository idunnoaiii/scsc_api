
from sqlalchemy import Column, ForeignKey, Integer, String, Float, sql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import BIGINT, BigInteger, Boolean, DateTime
from app.db.base_class import Base
from app.models.item import Item
from app.models.user import User


class Order(Base):
    __tablename__ = "orders"
    code = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    subtotal = Column(Integer, default=0)
    total = Column(Integer, default=0)
    discount = Column(Integer, default=0)
    order_items = relationship("OrderItem", back_populates="order")
    user = relationship("User", primaryjoin="User.id == Order.user_id")
    created_date = Column(DateTime, default=sql.func.now())
    updated_date = Column(DateTime, default=sql.func.now())    
    #try test add a colum with type BIGINT


orders = Order.__table__


class OrderItem(Base):
    __tablename__ = 'orderitems'
    order_id = Column(Integer, ForeignKey("orders.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    price = Column(Integer)
    quantity = Column(Integer)
    item_name = Column(String(length=100))
    order = relationship("Order", back_populates="order_items")


order_items = OrderItem.__table__
