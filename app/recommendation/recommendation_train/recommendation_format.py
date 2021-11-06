from typing import Dict, List

import numpy as np

from .collection_helper import CollectionHelper


def recommendation_format_to_user(
        recommended_items: np.array,
        books_collection: CollectionHelper,
        rubrics_collection: CollectionHelper,
        user: dict,
        size_recommendation: int = 50,
) -> Dict[str, List]:
    books_ids_from_books = []
    for book_col in recommended_items:
        _book = books_collection.get_item_from_index(book_col)
        if _book:
            books_ids_from_books.append(_book["id"])

    book_ids_from_rubrics = []

    for _book_id in user["books"]:
        book = books_collection.get_item_from_id(_book_id)

        if book:
            rubric_id = book.get("rubric_id")
            if rubric_id:
                rubric = rubrics_collection.get_item_from_id(rubric_id)
                book_ids_from_rubrics.extend(rubric["books"])

    user_books = user["books"]

    if len(books_ids_from_books) > 0:
        books_crossing = (set(book_ids_from_rubrics) & set(books_ids_from_books)) - set(user_books)
        if len(books_crossing) == 0:
            _recommendation_book_ids = set(books_ids_from_books) - set(user_books)

        else:
            _recommendation_book_ids = books_crossing

    else:
        _recommendation_book_ids = set(book_ids_from_rubrics) - set(user_books)

    recommendation_books = []

    # сохраняем ранжирование
    for _book_id in books_ids_from_books:
        if _book_id in _recommendation_book_ids:
            recommendation_books.append(_book_id)
            _recommendation_book_ids.remove(_book_id)

    recommendation_books.extend(list(_recommendation_book_ids))

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

        if i > size_recommendation:
            break

    for i, book_id in enumerate(recommendation_books):
        _book = books_collection.get_item_from_id(book_id)
        if _book:
            user_data["recommendations"].append({
                "id": _book["id"],
                "title": _book["title"],
                "author": _book["author"]
            })

        if i > size_recommendation:
            break

    return user_data
