from typing import List
from app.repositories.base import RepoBase
from app.models.discount import Discount
from app.schemas import DiscountCreate, DiscountUpdate
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import DiscountModel


class DiscountRepo(RepoBase[Discount, DiscountCreate, DiscountUpdate]):
    
    def get_all(
        self, db: Session,
    ) -> List[DiscountModel]:
        return db.query(DiscountModel) \
        .filter(and_(DiscountModel.is_active == True , DiscountModel.is_apply == True)) \
        .order_by(DiscountModel.threshold.desc()).all()

discount = DiscountRepo(Discount)