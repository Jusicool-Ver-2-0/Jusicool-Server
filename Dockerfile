FROM python:3.11

WORKDIR /app

COPY . /app

RUN apt update && apt upgrade -y

RUN pip install --upgrade pip

RUN pip install poetry

RUN poetry install --no-root

EXPOSE 8000

RUN chmod +x ./docker-entrypoint.sh

CMD [ "./docker-entrypoint.sh" ]