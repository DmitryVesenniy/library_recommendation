from typing import Generator, Dict

import ijson


def extract_json(filename) -> Generator:
    with open(filename, 'rb') as input_file:
        jsonobj = ijson.items(input_file, 'item')
        jsons = (o for o in jsonobj)

        for j in jsons:
            yield j


