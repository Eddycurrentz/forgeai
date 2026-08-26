PYTHON ?= python
PIP ?= pip
NPM ?= npm

.PHONY: help install install-web env up down logs api web test lint format typecheck migrate

help:
	@echo "ForgeAI Phase 1 targets"
	@echo "  make env          Copy .env.example to .env if missing"
	@echo "  make install      Install API and shared packages (editable) plus dev tools"
	@echo "  make install-web  Install Next.js dependencies"
	@echo "  make up           Start Docker Compose stack"
	@echo "  make down         Stop Docker Compose stack"
	@echo "  make api          Run API with uvicorn on :8000"
	@echo "  make web          Run Next.js dev server"
	@echo "  make test         Run pytest"
	@echo "  make lint         Run Ruff"
	@echo "  make format       Format with Ruff"
	@echo "  make typecheck    Run MyPy"
	@echo "  make migrate      Run Alembic upgrade head"

env:
	@if [ ! -f .env ]; then cp .env.example .env; fi

install: env
	$(PIP) install -e packages/shared -e "./apps/api[dev]"

install-web:
	cd apps/web && $(NPM) install

up: env
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

api:
	cd apps/api && uvicorn forgeai_api.main:app --reload --host 0.0.0.0 --port 8000

web:
	cd apps/web && $(NPM) run dev

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check apps/api/src packages/shared/src tests

format:
	$(PYTHON) -m ruff format apps/api/src packages/shared/src tests
	$(PYTHON) -m ruff check --fix apps/api/src packages/shared/src tests

typecheck:
	$(PYTHON) -m mypy

migrate:
	cd apps/api && alembic upgrade head
