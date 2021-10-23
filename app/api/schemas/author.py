from pydantic import BaseModel


class Author(BaseModel):
    id: int = None
    author_fullName: str = None
