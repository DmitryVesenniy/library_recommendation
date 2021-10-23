import os
import json
from typing import List, Dict, Union


class CollectionHelper:
    def __init__(self, collection: List[Dict], field_id: str = "id", indexing: bool = True):
        self.field_id = field_id
        self._collection = collection
        self._collection_ref = {}
        self._indexes = {}

        if indexing:
            self.create_indexes()

        self.length = len(self._collection)

    def create_indexes(self):
        for i, item in enumerate(self._collection):
            self._indexes[item[self.field_id]] = i

    def get_index(self, item_id: int) -> int:
        return self._indexes.get(item_id)

    def get_item_from_id(self, item_id: int) -> Union[Dict, None]:
        index = self._indexes.get(item_id, None)
        if index is not None:
            return self._collection[index]

        return None

    def get_item_from_index(self, index: int) -> dict:
        if len(self._collection) - 1 > index:
            return self._collection[index]

    @property
    def collection_ids(self):
        return list(map(lambda item: item[self.field_id], self._collection))

    @property
    def collection(self):
        return self._collection

    def save_to_file(self, path: str, filename: str):
        data_save = {
            "collection": self._collection,
            "indexes": self._indexes,
            "field_id": self.field_id,
        }

        if not os.path.isdir(path):
            os.mkdir(path)

        with open(os.path.join(path, filename), 'w') as f:
            f.write(json.dumps(data_save))

    @staticmethod
    def load_collection(file_path: str) -> 'CollectionHelper':
        with open(file_path, 'r') as f:
            data = json.loads(f.read())

        collection = CollectionHelper(data["collection"], data["field_id"], False)
        collection._indexes = {int(key): int(data["indexes"][key]) for key in data["indexes"]}

        return collection
