from sqlalchemy import Date, Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

from db.base_db import Base


class Users(Base):
    id = Column(Integer, primary_key=True, index=True)
    address = Column(VARCHAR(500), nullable=True)
    year_of_birth = Column(Date, nullable=True)
    circulation = relationship("Circulating", order_by='desc(Circulating.start_date)')
    recommendations = relationship("Recommendations")
