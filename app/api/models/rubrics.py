from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

from db.base_db import Base


class Rubrics(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(200), nullable=False)
