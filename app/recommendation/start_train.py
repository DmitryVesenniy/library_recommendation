from recommendation_train.train import train
from variables import (
    DATA_PATH,
    DATA_SET_PATH,
    USER_DB_PATH,
    BOOKS_COLLECTION_FILE,
    RUBRICS_COLLECTION_FILE,
    USERS_COLLECTIONS_FILE,
    SPARSE_MATRIX_FILE,
    CALCULATE_ALL,
)


def main():
    train(
        DATA_PATH,
        DATA_SET_PATH,
        USER_DB_PATH,
        BOOKS_COLLECTION_FILE,
        RUBRICS_COLLECTION_FILE,
        USERS_COLLECTIONS_FILE,
        SPARSE_MATRIX_FILE,
        CALCULATE_ALL,
    )


if __name__ == "__main__":
    main()
