from scipy import sparse
from sklearn.neighbors import NearestNeighbors
from pydantic import BaseModel

from settings import BASE_PATH
from . import depends
from .interface import StateApp

from recommendation_train.collection_helper import CollectionHelper
from variables import (
    USER_DB_PATH,
    SPARSE_MATRIX_FILE,
    BOOKS_COLLECTION_FILE,
    RUBRICS_COLLECTION_FILE,
    USERS_COLLECTIONS_FILE,
)

STATE = StateApp()


def init():
    books_collection = CollectionHelper.load_collection(BOOKS_COLLECTION_FILE)
    rubrics_collection = CollectionHelper.load_collection(RUBRICS_COLLECTION_FILE)
    users_collection = CollectionHelper.load_collection(USERS_COLLECTIONS_FILE)
    matrix = sparse.load_npz(SPARSE_MATRIX_FILE)
    knn = NearestNeighbors(n_neighbors=500, metric="cosine", n_jobs=-1)
    knn.fit(matrix)

    STATE.books_collections = books_collection
    STATE.rubrics_collections = rubrics_collection
    STATE.users_collections = users_collection
    STATE.matrix_train = matrix
    STATE.knn = knn
