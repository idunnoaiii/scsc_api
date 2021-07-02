from sqlalchemy import Column, ForeignKey, Integer, String, Float, sql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table
from sqlalchemy.sql.sqltypes import DateTime
from app.db.base_class import Base


# class Category(Base):
#     __tablename__ = "categories"
#     name = Column(String, index=True, )
#     description = Column(String, nullable=True)
#     items = relationship("Item", back_populates="items")
 
 
association_table = Table('categoryitems', Base.metadata,
    Column('category_id', Integer, ForeignKey('categories.id')),
    Column('item_id', Integer, ForeignKey('items.id'))
)

class Category(Base):
    __tablename__ = "categories"
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_date = Column(DateTime, default=sql.func.now())
    updated_date = Column(DateTime, default=sql.func.now())
    
    items = relationship("Item", secondary=association_table, back_populates="categories")




categories = Category.__table__