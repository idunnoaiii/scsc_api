from fastapi.param_functions import Query
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Connection, Transaction
from sqlalchemy.sql.expression import insert
from app.repositories import item_repo, order_repo
from app.core.config   import settings
from app.db.session import SessionLocal, engine
from app.models import OrderModel, orders_table, order_item_table, OrderItemModel
from app.schemas import ItemCreate
from sqlalchemy import select, text, inspect
from sqlalchemy.orm import aliased

db : Session = SessionLocal()
# list_order = db.query(OrderModel).filter(OrderModel.code is None)

#---------------------------SELECT---------------------------------------
# with engine.connect() as conn, conn.begin() as tran:
#     conn: Connection
#     tran: Transaction

# find_order = select([OrderModel.id]).where(OrderModel.code == None)
# t = text("SELECT * FROM orders")
# rs = db.execute(t)
# print(rs.fetchone())
# print(type(rs.fetchone()))
# for o in orders_list:
#     print(type(o))


#---------------------------UPDATE---------------------------------------

# stmt = orders_table.select().where(orders_table.c.id == 1)
# rs = db.execute(stmt)
# print(rs.fetchone())


# stmt2 = orders_table.update().where(orders_table.c.id == 1).values(tax = 80)
# db.execute(stmt2)
# db.commit()


# stmt = orders_table.select().where(orders_table.c.id == 1)
# rs = db.execute(stmt)
# print(rs.fetchone())

# db.close()

#--------------------------JOIN----------------------------------------------
# # rs = db.query(OrderModel).outerjoin(OrderItemModel).all()
# # rs2 = db.query(OrderModel).all()
# # print(inspect(stmt))
# # rs = db.execute(stmt).fetchall()
# # for item in rs:
# #     print(item)
# # print("----------------------------------------------")
# # for item in rs2: 
# #     print(item)
# # db.close()


#---------------------------INSPECT--------------------------
o = aliased(OrderModel, nam)
print(inspect(o))

