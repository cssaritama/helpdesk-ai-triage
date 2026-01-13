SHELL := /bin/bash

.PHONY: help up down logs ps lint test test-backend test-frontend test-integration gen-openapi seed

help:
	@echo "Targets:"
	@echo "  make up               - Start full system via docker-compose"
	@echo "  make down             - Stop system"
	@echo "  make logs             - Follow logs"
	@echo "  make test             - Run backend+frontend tests (container-free)"
	@echo "  make test-integration - Run integration tests via docker-compose (Postgres)"
	@echo "  make gen-openapi      - Export OpenAPI spec into docs/api/openapi.yaml"
	@echo "  make seed             - Seed KB with sample articles (local backend required)"

up:
	docker compose up --build -d

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

test: test-backend test-frontend

test-backend:
	cd backend && python -m pytest -q

test-frontend:
	cd frontend && npm test

test-integration:
	docker compose -f docker-compose.yml -f docker-compose.test.yml up --build -d db backend
	cd backend && INTEGRATION=1 DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/app python -m pytest -q tests/integration
	docker compose -f docker-compose.yml -f docker-compose.test.yml down -v

gen-openapi:
	bash scripts/export_openapi.sh

seed:
	python scripts/seed_kb.py
