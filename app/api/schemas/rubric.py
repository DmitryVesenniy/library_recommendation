from pydantic import BaseModel


class Rubric(BaseModel):
    id: int = None
    name: str = None
