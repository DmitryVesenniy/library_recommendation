import os

from utils.transform_data import transform_to_valid_data, save_valid_data
from variables import BASE_PATH, BOOKS_DATA_JSN, DATA_PATH


def main():
    books, rubrics, collapsed_ref_ids, collapse_field = transform_to_valid_data(BOOKS_DATA_JSN)

    save_valid_data(os.path.join(DATA_PATH, "books.json"), books)
    save_valid_data(os.path.join(DATA_PATH, "rubrics.json"), rubrics)
    save_valid_data(os.path.join(DATA_PATH, "collapsed_ref_ids.json"), collapsed_ref_ids)
    save_valid_data(os.path.join(DATA_PATH, "collapse_field.json"), collapse_field)


if __name__ == "__main__":
    main()
