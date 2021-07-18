
from sqlalchemy import Column, ForeignKey, Integer, String, Float, sql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from app.db.base_class import Base
from app.models.category import association_table 


# class Category(Base):
#     __tablename__ = "categories"
#     name = Column(String, index=True)
#     description = Column(String, nullable=True)
#     items = relationship("Item", back_populates="items")
 

class Item(Base):
    __tablename__ = "items"
    name = Column(String(length=200), index=True)
    slug = Column(String(length=200))
    description = Column(String, nullable=True)
    price = Column(Float, default=0)
    image_url = Column(String)
    quantity = Column(Integer, default=0)
    stock = Column(Boolean, default=False)
    created_date = Column(DateTime, default=sql.func.now())
    updated_date = Column(DateTime, default=sql.func.now())
    categories = relationship("Category", secondary=association_table, back_populates="items")


items = Item.__table__