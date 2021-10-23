from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.base_db import Base


class Circulating(Base):
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), nullable=False, index=True)
    book = relationship("Books")
    reader_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

