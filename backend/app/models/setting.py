
from sqlalchemy import Boolean, Column, Integer, String, sql
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.sql.sqltypes import DateTime

class Setting(Base):
    __tablename__ = "settings"
    store_name = Column(String)
    adddress: Column(String)
    phone = Column(Integer)
    footer = Column(String)
    created_date = Column(DateTime, default=sql.func.now())
    updated_date = Column(DateTime, default=sql.func.now())

settings = Setting.__table__