#!/usr/bin/env bash

source ./venv/bin/activate &&
  cd app/api &&
  python -m gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app -b "0.0.0.0:8000"
# python ./app/api/main.py
