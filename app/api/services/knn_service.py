import json
import random
from typing import Dict, List

import numpy as np

from global_state.state import STATE


def get_neighbors(index: int, n: int) -> np.array:
    row = STATE.matrix_train.getrow(index)
    knn_result = STATE.knn.kneighbors(row, n_neighbors=n)
    neighbors = knn_result[1]
    scores = np.asarray(STATE.matrix_train.tocsr()[neighbors[0]].sum(axis=0)[0]).flatten()
    top_indices = np.argsort(-scores)
    recommended_items = top_indices[:500]

    return recommended_items


def get_top_books(filename: str, count: int) -> Dict[str, List]:
    with open(filename, 'r') as f:
        recommendation = json.loads(f.read())
        books = recommendation["recommendations"]
        random.shuffle(books)
    return {
        "recommendations": books[:count]
    }
