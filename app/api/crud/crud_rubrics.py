from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder
from .base import CRUDBase
from models.rubrics import Rubrics
from schemas.rubric import Rubric


class RubricService(CRUDBase[Rubrics, Rubric]):
    def create(self, db: Session, rubric_obj: Rubric) -> Rubrics:
        obj_in_data = jsonable_encoder(rubric_obj)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


rubrics_service = RubricService(Rubrics)
