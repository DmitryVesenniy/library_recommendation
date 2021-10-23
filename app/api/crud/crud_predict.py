from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from db.session import database
from .base import CRUDBase
from models.users import Users
from models.circulation import Circulating
from models.recommendation import Recommendations
from schemas.predict import Recommendation


class RecommendationService(CRUDBase[Users, Recommendation]):
    async def get_user_recommendation_data(
            self, db: Session, user_id: int, limit: int = 100
    ) -> Recommendation:
        query = select(self.model).filter(Users.id == user_id).options(
            joinedload(self.model.recommendations),
            joinedload(self.model.circulation).joinedload(Circulating.book),
        )
        # return db.query(self.model).filter(Users.id == user_id).options(
        #     joinedload(self.model.recommendations),
        #     joinedload(self.model.circulation).joinedload(Circulating.book),
        # )
        return await database.fetch_one(query)


recommendation_service = RecommendationService(Users)
