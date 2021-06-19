
import databases
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from app.core.config import settings

database = databases.Database(settings.DATABASE_URL_ASYNC)
Base: DeclarativeMeta = declarative_base()