# Makefile

.PHONY: help postgres-up postgres-down mongo-up mongo-down logs-postgres logs-mongo

help:
	@echo "Comandos disponíveis:"
	@echo "  make postgres-up     - Iniciar ambiente PostgreSQL"
	@echo "  make postgres-down   - Parar ambiente PostgreSQL"
	@echo "  make mongo-up        - Iniciar ambiente MongoDB"
	@echo "  make mongo-down      - Parar ambiente MongoDB"
	@echo "  make logs-postgres   - Ver logs do PostgreSQL"
	@echo "  make logs-mongo      - Ver logs do MongoDB"
	@echo "  make stop-all        - Parar todos os ambientes"

postgres-up:
	docker compose up -d --build
	docker compose logs -f api

postgres-down:
	docker compose down

mongo-up:
	docker compose -f docker-compose.mongo.yml up -d --build
	docker compose -f docker-compose.mongo.yml logs -f api

mongo-down:
	docker compose -f docker-compose.mongo.yml down

logs-postgres:
	docker compose logs -f

logs-mongo:
	docker compose -f docker-compose.mongo.yml logs -f

stop-all:
	docker compose down
	docker compose -f docker-compose.mongo.yml down

psql:
	docker exec -it umlaramigo-db psql -U umlaramigo -d umlaramigo

mongosh:
	docker exec -it umlaramigo-mongodb mongosh -u umlaramigo -p umlaramigo_password