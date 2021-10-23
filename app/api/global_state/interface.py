from typing import Optional, Any

from pydantic import BaseModel

from scipy import sparse
from sklearn.neighbors import NearestNeighbors


class StateApp(BaseModel):
    books_collections: Optional[Any]
    rubrics_collections: Optional[Any]
    users_collections: Optional[Any]
    matrix_train: Optional[Any]
    knn: Optional[Any]

