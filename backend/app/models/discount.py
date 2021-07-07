
from sqlalchemy import Boolean, Column, Integer, String, sql, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.sql.sqltypes import DateTime

class Discount(Base):
    __tablename__ = "discounts"
    description = Column(String)
    threshold = Column(Integer, default=0, nullable=False)
    type = Column(Integer, default=0, nullable=False)
    value = Column(Float, default=0, nullable=False)
    is_apply = Column(Boolean, default=False)
    created_date = Column(DateTime, default=sql.func.now())
    updated_date = Column(DateTime, default=sql.func.now())

discount = Discount.__table__