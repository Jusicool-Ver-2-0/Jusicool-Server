#!/bin/bash

echo "migrate"
poetry run python ./src/manage.py migrate

echo "start celery worker"
poetry run celery --workdir src -A core.celery worker --loglevel=info

echo "start celery beat"
poetry run celery --workdir src -A core.celery beat --loglevel=info --scheduler celery.beat:Scheduler

echo "start application"
poetry run gunicorn --chdir ./src/ -b 0.0.0.0:8000 core.wsgi:application