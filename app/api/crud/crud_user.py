from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder
from .base import CRUDBase
from models.users import Users
from schemas.user import User


class RubricService(CRUDBase[Users, User]):
    def create(self, db: Session, user_obj: User) -> Users:
        obj_in_data = jsonable_encoder(user_obj)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user_service = RubricService(Users)