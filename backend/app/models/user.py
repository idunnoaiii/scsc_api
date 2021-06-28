
from sqlalchemy import Boolean, Column, Integer, String, sql
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.sql.sqltypes import DateTime

class User(Base):
    __tablename__ = "users"
    full_name = Column(String, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean(), default=False)
    created_date = Column(DateTime, default=sql.func.now())
    updated_date = Column(DateTime, default=sql.func.now())

users = User.__table__