from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models
from app.repositories import user_repo
from app.schemas.user import TokenPayload
import app.utils as settings
from app.core.config import settings
from app.db.session import SessionLocal
import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials
from app.core.config import settings
import redis

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.UserModel:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_repo.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



def get_current_active_user(
    current_user: models.UserModel = Depends(get_current_user),
) -> models.UserModel:
    if not user_repo.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_admin(
     db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_active_user),
) -> models.UserModel:
    if not user_repo.is_admin(db, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_firebase_bucket():
    if not firebase_admin._apps:
        cred = credentials.Certificate("certification.json")
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'scscbakery.appspot.com'
        })
    bucket = storage.bucket()
    return bucket 



def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            # host="redis-10572.c292.ap-southeast-1-1.ec2.cloud.redislabs.com",
            # port=10572,
            # password=settings.REDIS_PASSWORD,
            host='localhost',
            port=6379,
            db=0,
        )
        ping = client.ping()
        if ping is True:
            return client
    except Exception as e:
        print(e)



