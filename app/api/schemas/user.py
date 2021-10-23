from pydantic import BaseModel


class User(BaseModel):
    id: int = None
    address: str = None
    year_of_birth: str = None
