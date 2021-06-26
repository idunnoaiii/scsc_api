from sqlalchemy import Column, ForeignKey, Integer, String, Float, sql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from app.db.base_class import Base


# class Category(Base):
#     __tablename__ = "categories"
#     name = Column(String, index=True, )
#     description = Column(String, nullable=True)
#     items = relationship("Item", back_populates="items")
 

class Category(Base):
    __tablename__ = "categories"
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)


categories = Category.__table__