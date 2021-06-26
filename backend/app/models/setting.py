
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Setting(Base):
    __tablename__ = "settings"
    store_name = Column(String)
    adddress: Column(String)
    phone = Column(Integer)
    footer = Column(String)


settings = Setting.__table__