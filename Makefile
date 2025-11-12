.PHONY: help
.DEFAULT_GOAL := help

# Internal targets (used by other commands, not shown in help)
.PHONY: setup-env start-bg migrate createsuperuser generate-data

setup-env:
	@[ ! -f ./.env ] && cp ./.env.example ./.env || echo ".env file already exists."

start-bg:
	@docker-compose up -d

migrate:
	@echo "Running database migrations..."
	@docker-compose run --rm web python manage.py migrate

createsuperuser:
	@echo "Creating Django superuser..."
	@docker-compose run --rm web python manage.py createsuperuser

generate-data:
	@echo "Generating sample data..."
	@docker-compose run --rm web python manage.py generate_sample_data

# Public targets (shown in help)
init: setup-env build start-bg migrate createsuperuser generate-data stop start ## Quick setup (build, migrate, create superuser, generate sample data, and start server)

build: ## Build Docker containers
	@echo "Building Docker containers..."
	@docker-compose build

start: ## Start containers and show logs
	@echo "Starting the docker containers"
	@docker-compose up

stop: ## Stop containers
	@docker-compose down

clean: ## Remove containers and volumes
	@docker-compose down -v

test: ## Run all tests
	@docker-compose run --rm web python manage.py test --settings=config.settings_test ${ARGS}

dbshell: ## Open PostgreSQL shell
	@docker-compose exec db psql -U postgres wingz_rides

help: ## Show this help message
	@grep -hE '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
