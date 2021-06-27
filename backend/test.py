from app.repositories import item_repo, order_repo
from app.core.config   import settings
from app.db.session import SessionLocal
from app.models import items
from app.schemas import ItemCreate

session = SessionLocal()

list_item = item_repo.get_multi(session, skip=0, limit=100)
list_order = order_repo.get_multi(session, skip=0, limit=100)

for i in list_order:
    print(i.name)