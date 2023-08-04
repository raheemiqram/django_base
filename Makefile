SHELL=/bin/bash
.DEFAULT_GOAL := help


.PHONY: recreate-db
recreate-db: ## LOCAL - Drops the database and user and reloads the database export
recreate-db: drop-db reload-db-data migrate

redo-db: drop-db create-db silent_run migrate load_initial_data run

.PHONY: makemigrations
makemigrations: ## LOCAL - Perform django makemigrations in containers.
	docker-compose exec web python manage.py makemigrations --no-input

initial_setup: create-db migrate run

.PHONY: migrate
migrate: ## LOCAL - Perform django migrate in containers.
	docker-compose up -d web
	docker-compose exec web python manage.py migrate --no-input

.PHONY: reload-db-data
reload-db-data: ## LOCAL - Reload the database data
	docker-compose exec db createdb -U kmmrce kmmrce
	docker-compose exec db psql --user=kmmrce --dbname=kmmrce --file=/var/lib/postgresql/kmmrce.dump

create-db:
	docker-compose exec db createdb -U django_base django_base


.PHONY: drop-db
drop-db: ## LOCAL - Drop the database
	docker-compose up -d db
	docker-compose stop web
	docker-compose exec db dropdb -U django_base django_base

deploy:
	git pull
	pip install -r requirements/base.txt
	python manage.py migrate --no-input
	python manage.py collectstatic --no-input
	sudo service celery restart
	sudo service gunicorn restart

pre-commit:
	pre-commit run --all-files

run:
	docker-compose build
	docker-compose up
	docker-compose start


silent_run:
	docker-compose stop web
	docker-compose build
	docker-compose up --no-start --remove-orphans
	docker-compose start

prune:
	docker system prune --force


load_initial_data:
	docker-compose exec web python manage.py test_data


collectstatic:
	docker-compose exec web python manage.py collectstatic