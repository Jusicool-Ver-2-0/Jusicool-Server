FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install --no-root

EXPOSE 8000

RUN chmod +x ./docker-entrypoint.sh

CMD [ "./docker-entrypoint.sh" ]