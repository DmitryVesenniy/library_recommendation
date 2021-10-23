#!/usr/bin/env bash

source ./venv/bin/activate &&
  cd app/api &&
  python -m gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
# python ./app/api/main.py
