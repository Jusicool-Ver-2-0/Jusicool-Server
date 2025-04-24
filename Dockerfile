FROM python:3.13

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install --no-root

CMD poetry run python ./src/manage.py migrate && \\
    poetry run gunicorn --chdir src core.asgi:application -b 0.0.0.0:8000