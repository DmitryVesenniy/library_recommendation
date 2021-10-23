from sqlalchemy import Column, Integer, Text, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from db.base_db import Base


class Authors(Base):
    id = Column(Integer, primary_key=True, index=True)
    author_fullName = Column(VARCHAR(200), nullable=False)
