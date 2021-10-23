from sqlalchemy import Column, Integer, Text, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from db.base_db import Base
from .rubrics import Rubrics
from .authors import Authors


class Books(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(200), nullable=True)
    smart_collapse_field = Column(VARCHAR(50), nullable=True)
    author = Column(VARCHAR(200), nullable=True)
    annotation = Column(Text, nullable=True)
    rubric_id = Column(Integer, ForeignKey('rubrics.id', ondelete='CASCADE'), nullable=True, index=True)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete='CASCADE'), nullable=True, index=True)
    # rubric = Column(Integer, ForeignKey('rubrics.id', ondelete='CASCADE'), nullable=True, index=True)
    rubric = relationship(Rubrics)
    author = relationship(Authors)
