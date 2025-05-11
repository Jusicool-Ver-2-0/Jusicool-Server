FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install --no-root

CMD sh -c "poetry run python ./src/manage.py migrate && \
           poetry run gunicorn --chdir src core.wsgi:application -b 0.0.0.0:8000 && \
           poetry run celery --workdir src -A celery worker --loglevel=info --scheduler celery.beat:Scheduler &&\
           poetry run celery --workdir src -A celery beat --loglevel=info --scheduler celery.beat:Scheduler"