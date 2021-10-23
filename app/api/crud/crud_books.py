from typing import List

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from fastapi.encoders import jsonable_encoder
from .base import CRUDBase
from models.books import Books
from schemas.book import BookCreate


class BooksService(CRUDBase[Books, BookCreate, None]):
    def create(self, db: Session, book_obj: BookCreate) -> Books:
        obj_in_data = jsonable_encoder(book_obj)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_bulk(self, db: Session, books: List[BookCreate]) -> List[Books]:
        def convert_to(book: BookCreate):
            obj_in_data = jsonable_encoder(book)
            return self.model(**obj_in_data)

        db_objects = list(map(convert_to, books))
        db.add_all(db_objects)

        db.commit()
        return db_objects


books_service = BooksService(Books)
