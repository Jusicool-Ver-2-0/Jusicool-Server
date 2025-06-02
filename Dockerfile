FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --upgrade pip

RUN pip install poetry && poetry install --no-root

COPY . /app

EXPOSE 8000

RUN chmod +x ./docker-entrypoint.sh

CMD [ "./docker-entrypoint.sh" ]