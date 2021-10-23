from typing import Optional, List

from pydantic import BaseModel


# response predict
class InputUserId(BaseModel):
    id: Optional[int] = None


class ItemBooks(BaseModel):
    id: int = None
    title: str = None
    author: str = None


class Recommendation(BaseModel):
    recommendations: List[ItemBooks] = []
    history: List[ItemBooks] = []


class RequestModel(BaseModel):
    id: int
