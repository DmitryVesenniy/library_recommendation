import unittest

from core.deps import get_db
from schemas.book import BookCreate
from crud.crud_books import books_service

db = next(get_db())


class TestStringMethods(unittest.TestCase):

    def test_create_books(self):
        book = BookCreate(title="test", annotation="Live")
        book_obj = books_service.create(db, book)
        self.assertTrue(book_obj.id)


if __name__ == '__main__':
    unittest.main()
