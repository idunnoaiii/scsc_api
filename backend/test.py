from app.crud import order
from app.core.config   import settings
from app.db.session import SessionLocal
from app.models import items
from app.crud import item

session = SessionLocal()

list_item = item.get_multi(session, skip=0, limit=100)

for i in list_item:
    print(i.name)