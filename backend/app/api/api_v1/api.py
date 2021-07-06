 
from fastapi import APIRouter
from app.api.api_v1.endpoints import user
from app.api.api_v1.endpoints import item
from app.api.api_v1.endpoints import category
from app.api.api_v1.endpoints import order
from app.api.api_v1.endpoints import customer
from app.api.api_v1.endpoints import setting
from app.api.api_v1.endpoints import login

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(item.router, prefix="/items", tags=["items"])
api_router.include_router(order.router, prefix="/orders", tags=["orders"])
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
api_router.include_router(customer.router, prefix="/customers", tags=["customers"])
api_router.include_router(setting.router, prefix="/settings", tags=["settings"])
