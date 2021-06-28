from sqlalchemy import sql
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.ext.declarative.api import as_declarative, declared_attr
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer

# Base: DeclarativeMeta = declarative_base()


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
