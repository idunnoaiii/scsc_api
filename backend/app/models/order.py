
from sqlalchemy import Column, ForeignKey, Integer, String, Float, sql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from app.db.base_class import Base
from app.models.item import Item
from app.models.customer import Customer
from app.models.user import User


class Order(Base):
    __tablename__ = "orders"
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Boolean, default=0)
    tax = Column(Integer)
    subtotal = Column(Integer)
    paid = Column(Integer)
    change = Column(Integer)
    order_items = relationship("OrderItem", back_populates="order")


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

# class Association(Base):
#     __tablename__ = 'association'
#     left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
#     right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
#     extra_data = Column(String(50))
#     child = relationship("Child", back_populates="parents")
#     parent = relationship("Parent", back_populates="children")

# class Parent(Base):
#     __tablename__ = 'left'
#     id = Column(Integer, primary_key=True)
#     children = relationship("Association", back_populates="parent")

# class Child(Base):
#     __tablename__ = 'right'
#     id = Column(Integer, primary_key=True)
#     parents = relationship("Association", back_populates="child")