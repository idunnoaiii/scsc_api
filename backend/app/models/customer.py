
# from sqlalchemy import Boolean, Column, Integer, String, sql
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.sqltypes import DateTime
# from app.db.base_class import Base

# class Customer(Base):
#     __tablename__ = "customers"
#     name = Column(String, index=True, nullable=False)
#     contact = Column(String, unique=True, index=True, nullable=False)
#     address = Column(String)
#     created_date = Column(DateTime, default=sql.func.now())
#     updated_date = Column(DateTime, default=sql.func.now())

# customers = Customer.__table__


