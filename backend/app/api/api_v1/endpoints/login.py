from datetime import timedelta
import json
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.repositories import user_repo
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.utils import (
    generate_password_reset_token,
    verify_password_reset_token,
)
from pydantic import BaseModel
from app.api.deps import redis_connect

from uuid import uuid4

router = APIRouter()

redis_client = redis_connect()

@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:

    user = user_repo.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    print(user)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    elif not user_repo.is_active(db, user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    is_admin = user_repo.is_admin(db, user)
    if is_admin is not True:
        raise HTTPException(status_code=400, detail="Use not authorized")
    return {
        "access_token": security.create_access_token(
            json.dumps({"id": user.id, "is_admin": is_admin, "username": user.username}), expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


class LoginInfo(BaseModel):
    username: str = None
    password: str = None


@router.post("/login_qr")
def login_qr(
    db: Session = Depends(deps.get_db), login_info: LoginInfo = Body(...)
) -> Any:
    user = user_repo.authenticate(
        db, username=login_info.username, password=login_info.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    elif not user_repo.is_active(db, user):
        raise HTTPException(status_code=400, detail="Inactive user")
    is_customer = user_repo.is_customer(db, user)
    if is_customer is not True:
        raise HTTPException(status_code=400, detail="Use not authorized")
    token = uuid4()
    redis_client.execute_command("JSON.SET", "users", f".{user.username}", json.dumps(str(token)))
    return {
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "balance": user.balance,
        "token": token,
    }


class LogoutBody(BaseModel):
    username: str

@router.post("/logout_qr")
def logout_qr(
    logout_body: LogoutBody = Body(...),
    x_token: str = Header(...),
):
    try:
        user_key_token = redis_client.execute_command("JSON.GET", "users", f"{logout_body.username}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
    else:
        if user_key_token is None or user_key_token == "" or json.loads(user_key_token) != x_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
        redis_client.execute_command("JSON.SET", "users", f"{logout_body.username}", json.dumps(""))


# @router.post("/test-token", response_model=schemas.User)
# def test_token(current_user: models.UserModel = Depends(deps.get_current_user)) -> Any:
#     """
#     Test access token
#     """
#     return current_user


# @router.post("/password-recovery/{email}", response_model=schemas.Msg)
# def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
#     """
#     Password Recovery
#     """
#     user = crud.user.get_by_email(db, email=email)

#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     password_reset_token = generate_password_reset_token(email=email)
#     send_reset_password_email(
#         email_to=user.email, email=email, token=password_reset_token
#     )
#     return {"msg": "Password recovery email sent"}


# @router.post("/reset-password/")
# def reset_password(
#     token: str = Body(...),
#     new_password: str = Body(...),
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     Reset password
#     """
#     email = verify_password_reset_token(token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user = user_repo.get_by_username(db, email=email)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     elif not user_repo.is_active(user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     hashed_password = get_password_hash(new_password)
#     user.hashed_password = hashed_password
#     db.add(user)
#     db.commit()
#     return {"msg": "Password updated successfully"}
