
from sqlalchemy import Boolean, Column, Integer, String, sql, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.sql.sqltypes import DateTime


class Role(Base):
    __tablename__ = "roles"
    name = Column(String, unique=True)
    created_date = Column(DateTime, default=sql.func.now())
    updated_date = Column(DateTime, default=sql.func.now())
    

class User(Base):
    __tablename__ = "users"
    full_name = Column(String, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", primaryjoin="User.role_id == Role.id")
    address = Column(String)
    contact = Column(String)
    gender =  Column(Boolean, default=False)
    created_date = Column(DateTime, default=sql.func.now())
    updated_date = Column(DateTime, default=sql.func.now())


users = User.__table__

roles = Role.__table__