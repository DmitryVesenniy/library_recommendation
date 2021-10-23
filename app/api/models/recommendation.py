from sqlalchemy import Column, Integer, ForeignKey

from db.base_db import Base


class Recommendations(Base):
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
