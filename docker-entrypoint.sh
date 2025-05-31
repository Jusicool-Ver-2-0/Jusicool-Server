#!/bin/bash

echo "migrate"
poetry run python ./src/manage.py migrate

echo "start application"
poetry run gunicorn --chdir ./src/ -b 0.0.0.0:8000 core.wsgi:application