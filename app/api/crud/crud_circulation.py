from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder
from .base import CRUDBase
from models.circulation import Circulating
from schemas.circulate import Circulate


class CirculateService(CRUDBase[Circulating, Circulate]):
    ...
    # def create(self, db: Session, data_obj: Circulate) -> Circulating:
    #     obj_in_data = jsonable_encoder(data_obj)
    #     db_obj = self.model(**obj_in_data)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj


circulate_service = CirculateService(Circulating)
