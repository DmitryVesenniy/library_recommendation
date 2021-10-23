#!/usr/bin/env bash

source ./venv/bin/activate &&
    python ./app/recommendation/create_valid_json.py &&
    python ./app/recommendation/start_train.py
