makemigraions:
	poetry run python src/manage.py makemigrations

migrate:
	poetry run python src/manage.py migrate

lint:
	poetry run black src/
