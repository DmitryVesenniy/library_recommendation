#! /usr/bin/env bash
set -e

celery --app recommendation/celery_app beat&
