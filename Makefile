.PHONY: up down build logs shell db-shell redis-shell migrate generate help

# Default values
DC = docker compose
API_SERVICE = api_service
DB_CONTAINER = postgres
REDIS_CONTAINER = redis

help:
	@echo "Available commands:"
	@echo "  make up          - Start all containers in background"
	@echo "  make down        - Stop and remove all containers"
	@echo "  make build       - Rebuild the auth app image"
	@echo "  make logs        - Tail logs of all containers"
	@echo "  make api-shell   - Open a shell inside the auth api service"
	@echo "  make db-shell    - Open psql inside the postgres container"
	@echo "  make redis-shell - Open redis-cli inside the redis container"
	@echo "  make migrate     - Run Alembic migrations to head"
	@echo "  make generate    - Generate a new Alembic migration (usage: make generate m=\"message\")"

up:
	$(DC) up -d

down:
	$(DC) down

build:
	$(DC) build

logs:
	$(DC) logs -f

api-shell:
	docker exec -it $(API_SERVICE) /bin/sh

db-shell:
	docker exec -it $(DB_CONTAINER) psql -U postgres -d please_text_me_db

redis-shell:
	docker exec -it $(REDIS_CONTAINER) redis-cli

migrate:
	$(DC) exec -T $(API_SERVICE) alembic -c /app/alembic.ini upgrade head

generate:
	@if [ -z "$(m)" ]; then \
		echo "Error: Migration message is required. Usage: make generate m=\"migration message\""; \
		exit 1; \
	fi
	$(DC) exec -T $(API_SERVICE) alembic -c /app/alembic.ini revision --autogenerate -m "$(m)"