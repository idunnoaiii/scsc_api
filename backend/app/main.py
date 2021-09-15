from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from app.api.api_v1.api import api_router
from app.core.config import settings
import datetime
from app.api import deps
from app.repositories import item_repo
from app.db.session import SessionLocal
import json


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json", debug=True
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": "hello"}


@app.on_event("startup")
@repeat_every(seconds=60, wait_first=True)  # 1 hour
def build_redis_cache() -> None:
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0:
        redis = deps.redis_connect()
        if redis.ping() == False:
            return
        session = SessionLocal()
        items = item_repo.get_item_to_cache(session)
        session.close()
        if items is not None:
            with redis.pipeline() as rp:
                for item in items:
                    rp.execute_command("JSON.SET", item.id, '.', json.dumps({'id': item.id, 'name': item.name, 'price': item.price}))
                rp.execute()
