import os
import json
from typing import Dict

from settings import BASE_PATH
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.predict import Recommendation, RequestModel
from services.knn_service import get_neighbors, get_top_books

from global_state.state import STATE

router = APIRouter()

COUNT_BOOKS_AS_RESULT = 20


@router.post("/recommendation", response_model=Dict, status_code=200)
async def get_recommendation(user: RequestModel):
    file_name_user = os.path.join(BASE_PATH, f"db_users/{user.id}_data.json")
    file_name_top = os.path.join(BASE_PATH, f"db_users/top_data.json")

    if os.path.exists(file_name_user):
        try:
            with open(file_name_user, 'r') as f:
                return json.loads(f.read())

        except Exception as e:
            return {"error": str(e)}

    try:
        user_data = STATE.users_collections.get_item_from_id(int(user.id))

    except (TypeError, ValueError) as e:
        return {"error": str(e)}

    if not user_data:
        # загружаем топовые книги и рекомендуем их
        try:
            return get_top_books(file_name_top, 40)
        except Exception as e:
            return {"error": str(e)}

    row_index = STATE.users_collections.get_index(user_data["id"])

    recommended_items = get_neighbors(row_index, 500)

    books_ids_from_books = []
    for book_col in recommended_items:
        _book = STATE.books_collections.get_item_from_index(book_col)
        if _book:
            books_ids_from_books.append(_book["id"])

    book_ids_from_rubrics = []

    for _book_id in user_data["books"]:
        rubric_id = STATE.books_collections.get_item_from_id(_book_id).get("rubric_id")
        if rubric_id:
            rubric = STATE.rubrics_collections.get_item_from_id(rubric_id)
            book_ids_from_rubrics.extend(rubric["books"])

    user_books = user_data["books"]

    if len(books_ids_from_books) > 0:
        books_crossing = (set(book_ids_from_rubrics) & set(books_ids_from_books)) - set(user_books)
        if len(books_crossing) == 0:
            recommendation_book_ids = set(books_ids_from_books) - set(user_books)

        else:
            recommendation_book_ids = books_crossing

    else:
        recommendation_book_ids = set(book_ids_from_rubrics) - set(user_books)

    recommendation = {
        "recommendations": [],
        "history": [],
    }

    for i, book_id in enumerate(user_books):
        _book = STATE.books_collections.get_item_from_id(book_id)
        if _book:
            recommendation["history"].append({
                "id": _book["id"],
                "title": _book["title"],
                "author": _book["author"]
            })

    for i, book_id in enumerate(recommendation_book_ids):
        _book = STATE.books_collections.get_item_from_id(book_id)
        if _book:
            recommendation["recommendations"].append({
                "id": _book["id"],
                "title": _book["title"],
                "author": _book["author"]
            })

        if i > COUNT_BOOKS_AS_RESULT:
            break

    if len(recommendation["recommendations"]) == 0:
        # если мы не получили никаких рекомендаций, то советуем самые топовые книги
        top_books = get_top_books(file_name_top, 40)
        recommendation["recommendations"] = top_books["recommendations"]

    try:
        with open(file_name_user, 'w') as f:
            f.write(json.dumps(recommendation))
    except:
        pass

    return recommendation

