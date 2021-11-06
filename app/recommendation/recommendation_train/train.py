import os
import shutil
import json
from typing import Dict
from uuid import uuid1
from collections import defaultdict
from multiprocessing import Process, cpu_count

import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.neighbors import NearestNeighbors

from .collection_helper import CollectionHelper
from .csv_helpers import search_files


COUNT_BOOKS_AS_RESULT = 20
COUNT_BOOKS_AS_TOP = 200


def load_data(data_path: str):
    books = None
    rubrics = None
    collapsed_ref_ids = None

    with open(f"{data_path}/books.json", 'r') as f:
        books = json.loads(f.read())

    with open(f"{data_path}/rubrics.json", 'r') as f:
        rubrics = json.loads(f.read())

    with open(f"{data_path}/collapsed_ref_ids.json", 'r') as f:
        collapsed_ref_ids = json.loads(f.read())

    return books, rubrics, collapsed_ref_ids


def train(
        data_path: str,
        dataset_path: str,
        out_db: str,
        books_collection_file: str,
        rubrics_collection_file: str,
        users_collection_file: str,
        matrix_file: str,
        is_calculate_all: bool = False,
):

    if os.path.isdir(out_db):
        shutil.rmtree(out_db)

    os.mkdir(out_db)

    # загружаем ранее сформированные данные
    books, rubrics, collapsed_ref_ids = load_data(data_path)

    books_collection = CollectionHelper(books)
    rubrics_collection = CollectionHelper(rubrics)
    users_collection = get_user_collection(dataset_path, collapsed_ref_ids, books_collection)

    path_books_out, filename_books_out = os.path.split(books_collection_file)
    books_collection.save_to_file(path_books_out, filename_books_out)

    path_rubrics_out, filename_rubrics_out = os.path.split(rubrics_collection_file)
    rubrics_collection.save_to_file(path_rubrics_out, filename_rubrics_out)

    path_users_out, filename_users_out = os.path.split(users_collection_file)
    users_collection.save_to_file(path_users_out, filename_users_out)

    # строки - юзеры, столбцы - книги, в качестве значения - 1.0 или 0 (читал или нет)
    n_coll = 500
    rows = []
    for user_id in users_collection.collection_ids:
        rows.append(make_coo_row_books(users_collection.get_item_from_id(user_id)["books"], books_collection))

    user_book_sparse = sparse.vstack(rows).tocsr()
    path, filename = os.path.split(matrix_file)
    save_sparse(path, filename, user_book_sparse)

    # модель близости юзеров по взятым книгам книгам
    knn_book = NearestNeighbors(n_neighbors=n_coll, metric="cosine", n_jobs=-1)
    knn_book.fit(user_book_sparse)

    top_books_counter = defaultdict(int)
    top_rubrics_counter = defaultdict(int)

    if is_calculate_all:
        tasks = []
        chunk = int(len(users_collection.collection) / cpu_count()) + 1

        user_list = users_collection.collection

        for index_process in range(cpu_count()):
            print(f"!!! start process: {index_process + 1}")
            start_index = index_process * chunk
            end_index = start_index + chunk - 1
            proc = Process(target=user_item_recommendation, args=(
                user_list[start_index:end_index],
                rows,
                user_book_sparse,
                knn_book,
                users_collection,
                books_collection,
                rubrics_collection,
                n_coll,
                out_db,
            ))

            tasks.append(proc)
            proc.start()

        for proc in tasks:
            proc.join()

    for j, user in enumerate(users_collection.collection):
        for _book_id in user["books"]:
            top_books_counter[_book_id] += 1
            _book = books_collection.get_item_from_id(_book_id)
            top_rubrics_counter[_book["rubric_id"]] += 1

    # ищем среднего пользователя для холодного старта
    averages = (user_book_sparse.sum(0) / user_book_sparse.shape[0]).A

    knn_result = knn_book.kneighbors(averages, n_neighbors=n_coll)
    neighbors = knn_result[1]
    scores = np.asarray(user_book_sparse.tocsr()[neighbors[0]].sum(axis=0)[0]).flatten()
    top_indices = np.argsort(-scores)
    recommended_items_hold = top_indices[:500]

    books_ids_from_books = []
    for book_col in recommended_items_hold:
        _book = books_collection.get_item_from_index(book_col)
        if _book:
            books_ids_from_books.append(_book["id"])

    top_rubrics = list(top_rubrics_counter.keys())
    top_rubrics.sort(key=lambda x: top_rubrics_counter[x], reverse=True)
    top_rubrics = top_rubrics[:100]

    top_rubrics_book_ids = []
    for _rubric_id in top_rubrics:
        _rubric = rubrics_collection.get_item_from_id(_rubric_id)
        if _rubric:
            top_rubrics_book_ids.extend(_rubric["books"])

    top_recommendation = top_rubrics_book_ids

    top_books_result = {
        "recommendations": [],
    }
    for i, book_id in enumerate(top_recommendation):
        _book = books_collection.get_item_from_id(book_id)
        if _book:
            top_books_result["recommendations"].append({
                "id": _book["id"],
                "title": _book["title"],
                "author": _book["author"]
            })

        if i > COUNT_BOOKS_AS_TOP:
            break

    file_name = f"top_data.json"
    with open(os.path.join(out_db, file_name), 'w') as f:
        f.write(json.dumps(top_books_result))


def make_coo_row_books(read_books: list, books_indexes_helper: CollectionHelper):
    idx = []
    values = []

    for book_id in read_books:
        book = books_indexes_helper.get_item_from_id(book_id)
        if not book:
            continue
        idx.append(books_indexes_helper.get_index(book["id"]))
        values.append(1.0)

    return sparse.coo_matrix(
        (np.array(values).astype(np.float32), ([0] * len(idx), idx)), shape=(1, books_indexes_helper.length)
    )


def make_coo_row_rubrics(
        read_books: list,
        books_indexes_helper: CollectionHelper,
        rubrics_indexes_helper: CollectionHelper
):
    idx = []
    values = []
    counter_rubrics = defaultdict(int)

    # получаем количественное значение сколько раз книги каких рубрик пользователь читал
    for book_id in read_books:
        book = books_indexes_helper.get_item_from_id(book_id)
        if not book:
            continue

        rubric_id = book["rubric_id"]
        if not rubric_id:
            continue

        counter_rubrics[rubric_id] += 1

    for rubric_id in counter_rubrics:
        idx.append(rubrics_indexes_helper.get_index(rubric_id))
        values.append(counter_rubrics[rubric_id])

    return sparse.coo_matrix(
        (np.array(values).astype(np.float32), ([0] * len(idx), idx)), shape=(1, rubrics_indexes_helper.length)
    )


def get_user_collection(
        dataset_path: str,
        collapsed_ref_ids: Dict,
        books_collection: CollectionHelper
) -> CollectionHelper:
    """
    получаем информацию о всех пользователях и книгах, которые они читали
    :param dataset_path: str
    :param collapsed_ref_ids: Dict
    :param books_collection: CollectionHelper
    :return: CollectionHelper
    """
    circulation_files = search_files("circulaton", "csv", dataset_path)

    users_read_map = {}
    users = []

    for f in circulation_files:
        dataset = pd.read_csv(f"{dataset_path}/{f}", delimiter=";", low_memory=False, encoding='cp1251',
                              usecols=range(8))

        for i, data_row in enumerate(dataset.values):
            if not users_read_map.get(data_row[5]):
                users_read_map[data_row[5]] = []

            book_id = collapsed_ref_ids.get(data_row[1])
            if book_id:
                users_read_map[data_row[5]].append(book_id)

            elif books_collection.get_item_from_id(data_row[1]):
                users_read_map[data_row[5]].append(data_row[1])

    for idx, user_id in enumerate(users_read_map):
        users.append({
            "id": user_id,
            "books": users_read_map[user_id]
        })
    return CollectionHelper(users)


def save_sparse(path: str, filename: str, array: sparse.coo_matrix) -> None:
    if not os.path.isdir(path):
        os.mkdir(path)

    sparse.save_npz(os.path.join(path, filename), array)


def user_item_recommendation(
        user_items_list: list,
        rows: list,
        user_book_sparse: sparse,
        knn: NearestNeighbors,
        users_collection: CollectionHelper,
        books_collection: CollectionHelper,
        rubrics_collection: CollectionHelper,
        n_coll: int,
        out_db: str,
):
    uuid_path = str(uuid1())
    max_count_file_path = 50000
    current_count_file = 0

    os.mkdir(os.path.join(out_db, uuid_path))

    for j, user in enumerate(user_items_list):
        index = j
        row = rows[index]

        knn_result = knn.kneighbors(row, n_neighbors=n_coll)
        neighbors = knn_result[1]
        scores = np.asarray(user_book_sparse.tocsr()[neighbors[0]].sum(axis=0)[0]).flatten()
        top_indices = np.argsort(-scores)
        recommended_items = top_indices[:500]

        books_ids_from_books = []
        for book_col in recommended_items:
            _book = books_collection.get_item_from_index(book_col)
            if _book:
                books_ids_from_books.append(_book["id"])

        book_ids_from_rubrics = []

        for _book_id in user["books"]:

            rubric_id = books_collection.get_item_from_id(_book_id).get("rubric_id")
            if rubric_id:
                rubric = rubrics_collection.get_item_from_id(rubric_id)
                book_ids_from_rubrics.extend(rubric["books"])

        user_books = user["books"]

        if len(books_ids_from_books) > 0:
            books_crossing = (set(book_ids_from_rubrics) & set(books_ids_from_books)) - set(user_books)
            if len(books_crossing) == 0:
                recommendation_book_ids = set(books_ids_from_books) - set(user_books)

            else:
                recommendation_book_ids = books_crossing

        else:
            recommendation_book_ids = set(book_ids_from_rubrics) - set(user_books)

        user_data = {
            "recommendations": [],
            "history": [],
        }

        for i, book_id in enumerate(user_books):
            _book = books_collection.get_item_from_id(book_id)
            if _book:
                user_data["history"].append({
                    "id": _book["id"],
                    "title": _book["title"],
                    "author": _book["author"]
                })

            if i > COUNT_BOOKS_AS_RESULT:
                break

        for i, book_id in enumerate(recommendation_book_ids):
            _book = books_collection.get_item_from_id(book_id)
            if _book:
                user_data["recommendations"].append({
                    "id": _book["id"],
                    "title": _book["title"],
                    "author": _book["author"]
                })

            if i > COUNT_BOOKS_AS_RESULT:
                break

        file_name = f"{user['id']}_data.json"
        with open(os.path.join(out_db, uuid_path, file_name), 'w') as f:
            f.write(json.dumps(user_data))

        current_count_file += 1

        if current_count_file >= max_count_file_path:
            uuid_path = str(uuid1())
            current_count_file = 0
            os.mkdir(os.path.join(out_db, uuid_path))
