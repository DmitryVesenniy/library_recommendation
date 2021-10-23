import os
import sys
import configparser

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

config = configparser.ConfigParser()

config.read(os.path.join(BASE_PATH, "config.ini"))

try:
    DATA_SET_PATH = config['DEFAULT']['DATA_SET_PATH']
    DATA_PATH = config['DEFAULT']['DATA_PATH']
    BOOKS_DATA_JSN = config['DEFAULT']['BOOKS_DATA_JSN']
    CALCULATE_ALL = config['DEFAULT']['CALCULATE_ALL'] == "True"

except KeyError:
    print("Укажите обязательные поля в config.ini")
    sys.exit(1)

BASE_PROJECT = os.path.abspath(os.path.dirname(BASE_PATH))
DATA_SET_PATH = os.path.join(BASE_PATH, DATA_SET_PATH)
DATA_PATH = os.path.join(BASE_PATH, DATA_PATH)
BOOKS_DATA_JSN = os.path.join(BASE_PATH, BOOKS_DATA_JSN)
USER_DB_PATH = os.path.join(BASE_PROJECT, "api/db_users")

SPARSE_MATRIX_FILE = os.path.join(USER_DB_PATH, "arrays/user_book_sparse.npz")
BOOKS_COLLECTION_FILE = os.path.join(USER_DB_PATH, "collections/books_collection")
RUBRICS_COLLECTION_FILE = os.path.join(USER_DB_PATH, "collections/rubrics_collection")
USERS_COLLECTIONS_FILE = os.path.join(USER_DB_PATH, "collections/users_collection")
