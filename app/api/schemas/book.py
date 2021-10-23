from typing import Union, Optional

from pydantic import BaseModel

from .rubric import Rubric
from .author import Author


class BookCreate(BaseModel):
    id: int = None
    title: str = None
    smart_collapse_field: str = None
    author: str = None
    annotation: str = None
    rubric_id: Optional[int]
    author_id: Optional[int]
    rubric: Optional[Union[Rubric, str]]
    author: Optional[Union[Author, str]]
