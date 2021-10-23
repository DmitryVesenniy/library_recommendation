from pydantic import BaseModel


class Circulate(BaseModel):
    id: int = None
    start_date: str = None
    book_id: int = None
    reader_id: int = None
