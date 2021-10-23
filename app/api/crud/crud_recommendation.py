from .base import CRUDBase
from models.recommendation import Recommendations
from schemas.recommendation import RecommendationCreate


class RecommendationService(CRUDBase[Recommendations, RecommendationCreate]):
    ...
    # def create(self, db: Session, data_obj: Circulate) -> Circulating:
    #     obj_in_data = jsonable_encoder(data_obj)
    #     db_obj = self.model(**obj_in_data)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj


recommendation_service = RecommendationService(Recommendations)
