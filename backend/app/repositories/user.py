from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.security import get_password_hash, verify_password
from app.repositories.base import RepoBase
from app.models.user import User
from app.models import RoleModel
from app.schemas.user import UserCreate, UserUpdate


class UserRepo(RepoBase[User, UserCreate, UserUpdate]):

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).filter(and_(User.role_id == 2, User.is_active == True)).all()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_by_userid(self, db: Session, *, id: int) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()


    def create(self, db: Session, *, obj_in: UserCreate) -> User:

        db_obj = User(
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            roleid=obj_in.roleid,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True, exclude_none= True)
        # if update_data["password"]:
        #     hashed_password = get_password_hash(update_data["password"])
        #     del update_data["password"]
        #     update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)


    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


    def change_password(self, db: Session, *, username: str, new_password: str) -> None:
        user = self.get_by_username(db, username = username)
        new_password_hashed = get_password_hash(new_password)
        user.hashed_password = new_password_hashed
        db.commit()


    def is_active(self, db: Session, user: User) -> bool:
        db_obj = db.query(User).filter(User.id == user.id).first()
        return db_obj.is_active == True


    def is_admin(self, db: Session, user: User) -> bool:
        db_role = db.query(RoleModel).filter(RoleModel.id == user.role_id).first()
        return db_role.name == "admin"

    def is_customer(self, db: Session, user: User) -> bool:
        db_role = db.query(RoleModel).filter(RoleModel.id == user.role_id).first()
        return db_role.name == "customer"

    def get_roles(self, db: Session):
        return db.query(RoleModel).all()

    def login_qr(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def subtract_balance(self, db: Session, *, user_id: int, amount: int):
        user = db.query(User).filter(User.id == user_id).first()
        user.balance -= amount
        db.commit()


user = UserRepo(User)