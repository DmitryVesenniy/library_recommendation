from sqlalchemy.orm import Session

from models.users import Users
from models.books import Books
from models.rubrics import Rubrics
from models.authors import Authors
from models.circulation import Circulating
from models.recommendation import Recommendations
from db.base_db import Base


def init_db(db: Session) -> None:
    Base.metadata.create_all(db)
