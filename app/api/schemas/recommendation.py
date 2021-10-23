from pydantic import BaseModel


class RecommendationCreate(BaseModel):
    id: int = None
    book_id: int = None
    user_id: int = None
