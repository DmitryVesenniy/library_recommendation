from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import databases

from core import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine)
database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)