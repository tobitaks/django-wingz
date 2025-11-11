.PHONY: help
.DEFAULT_GOAL := help

setup-env: ## Setup .env file from .env.example
	@[ ! -f ./.env ] && cp ./.env.example ./.env || echo ".env file already exists."

build: ## Build Docker containers
	@echo "Building Docker containers..."
	@docker-compose build

start: ## Start the docker containers
	@echo "Starting the docker containers"
	@docker-compose up

start-bg: ## Run containers in the background
	@docker-compose up -d

stop: ## Stop containers
	@docker-compose down

restart: stop start ## Restart containers

logs: ## View logs from containers
	@docker-compose logs -f

ssh: ## SSH into running web container
	@docker-compose exec web bash

bash: ## Get a bash shell into the web container
	@docker-compose run --rm web bash

manage: ## Run any manage.py command. E.g. `make manage ARGS='createsuperuser'`
	@docker-compose run --rm web python manage.py ${ARGS}

migrations: ## Create DB migrations in the container
	@docker-compose run --rm web python manage.py makemigrations

migrate: ## Run DB migrations in the container
	@docker-compose run --rm web python manage.py migrate

shell: ## Get a Django shell
	@docker-compose run --rm web python manage.py shell

dbshell: ## Get a PostgreSQL shell
	@docker-compose exec db psql -U postgres wingz_rides

test: ## Run Django tests
	@docker-compose run --rm web python manage.py test ${ARGS}

createsuperuser: ## Create a Django superuser
	@docker-compose run --rm web python manage.py createsuperuser

loaddata: ## Load fixture data. E.g. `make loaddata ARGS='rides/fixtures/sample_data.json'`
	@docker-compose run --rm web python manage.py loaddata ${ARGS}

dumpdata: ## Dump data to fixture. E.g. `make dumpdata ARGS='rides --indent 2 > rides/fixtures/sample_data.json'`
	@docker-compose run --rm web python manage.py dumpdata ${ARGS}

clean: ## Remove containers and volumes
	@docker-compose down -v

rebuild: clean build start-bg ## Clean rebuild of containers

init: setup-env build start-bg migrate createsuperuser ## Quick setup (build, migrate, create superuser)

collectstatic: ## Collect static files
	@docker-compose run --rm web python manage.py collectstatic --noinput

check: ## Run Django system checks
	@docker-compose run --rm web python manage.py check

showmigrations: ## Show all migrations
	@docker-compose run --rm web python manage.py showmigrations

debug-queries: ## Show SQL queries (requires django-debug-toolbar)
	@echo "Django Debug Toolbar is enabled. Visit http://localhost:8000 and check the toolbar."

ps: ## Show running containers
	@docker-compose ps

help: ## Show this help message
	@grep -hE '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
