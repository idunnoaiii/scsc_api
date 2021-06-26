
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Customer(Base):
    __tablename__ = "customers"
    name = Column(String, index=True)
    phone = Column(Integer, unique=True, index=True, nullable=False)
    email = Column(String)
    address = Column(String)

customers = Customer.__table__