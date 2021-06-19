
from sqlalchemy import Column, ForeignKey, Integer, String, Float, sql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from app.db.base_class import Base


# class Category(Base):
#     __tablename__ = "categories"
#     name = Column(String, index=True)
#     description = Column(String, nullable=True)
#     items = relationship("Item", back_populates="items")
 

class Item(Base):
    __tablename__ = "items"
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, default=0)
    image_url = Column(String)
    expired_date = Column(DateTime, nullable=True, default=sql.func.now())
    # category_id = Column(Integer, ForeignKey("categories.id"))


items = Item.__table__