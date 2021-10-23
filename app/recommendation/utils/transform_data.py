import json
from typing import Tuple, List, Dict, Union

from .parse_big_json import extract_json


def transform_to_valid_data(path_in: str) -> Tuple[List[Dict], List[Dict], Dict, Dict]:
    gen = extract_json(path_in)

    collapse_field = {}
    collapsed_ref_ids = {}
    books = []
    rubrics_map = {}
    rubrics = []

    for book in gen:
        smart_collapse_field = book.get("smart_collapse_field")
        if not smart_collapse_field:
            books.append({
                "id": book["id"],
                "title": book["title"],
                "author": book["author_fullNameAlt"],
                "rubric_id": book["rubric_id"],
            })
        elif not collapse_field.get(smart_collapse_field):
            collapse_field[smart_collapse_field] = book["id"]
            books.append({
                "id": book["id"],
                "title": book["title"],
                "author": book["author_fullNameAlt"],
                "rubric_id": book["rubric_id"],
            })

            if book.get("rubric_id"):
                if not rubrics_map.get(book["rubric_id"]):
                    rubrics_map[book["rubric_id"]] = {
                        "books": [],
                        "rubric_name": book.get("rubric_name")
                    }
                rubrics_map[book["rubric_id"]]["books"].append(book["id"])

        collapsed_ref_ids[book["id"]] = collapse_field[smart_collapse_field]

    for _key in rubrics_map:
        rubrics.append({
            "id": _key,
            "books": rubrics_map[_key]["books"],
            "rubric_name": rubrics_map[_key]["rubric_name"],
        })

    return books, rubrics, collapsed_ref_ids, collapse_field


def save_valid_data(file_name: str, data: Union[List[Dict], Dict]):
    with open(file_name, "w") as f:
        f.write(json.dumps(data))

