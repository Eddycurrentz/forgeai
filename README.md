# ForgeAI

Industrial-grade autonomous AI software engineer. Phase 1 is the project foundation: a FastAPI health service, a Next.js operator shell, PostgreSQL, Redis, and the planning documents for later phases.

This repository does **not** yet implement agents, RAG, code indexing, sandboxed execution, or Git automation.

## Layout

```
forgeai/
├── apps/api/                 FastAPI service
├── apps/web/                 Next.js console
├── packages/                 Future domain packages (empty except shared)
├── infrastructure/           Extra infra assets (later phases)
├── tests/                    pytest suite
├── scripts/
├── docs/
├── docker-compose.yml
├── Makefile
├── AGENTS.md
├── ARCHITECTURE.md
├── TASKS.md
└── DECISIONS.md
```

## Prerequisites

- Python 3.12+
- Node.js 22+
- Docker and Docker Compose

## Environment

```powershell
Copy-Item .env.example .env
```

Unix:

```bash
cp .env.example .env
```

## Install dependencies

Python (from the repository root, preferably in a virtualenv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e packages/shared -e ".\apps\api[dev]"
```

Frontend:

```powershell
cd apps\web
npm install
```

## Start Docker Compose

From the repository root:

```powershell
docker compose up --build
```

This starts PostgreSQL, Redis, the API (`http://localhost:8000`), and the web app (`http://localhost:3000`).

Stop with `docker compose down`.

## Run the API locally

PostgreSQL and Redis must be reachable at the URLs in `.env` (Compose can provide them: `docker compose up postgres redis`).

```powershell
cd apps\api
uvicorn forgeai_api.main:app --reload --host 0.0.0.0 --port 8000
```

## Test the API

```powershell
curl http://localhost:8000/health
```

Expected JSON includes `status`, `postgres`, `redis`, and `version`. `status` is `ok` when both dependencies respond, otherwise `degraded`.

OpenAPI: `http://localhost:8000/docs`.

## Run the frontend

```powershell
cd apps\web
$env:NEXT_PUBLIC_API_URL = "http://localhost:8000"
npm run dev
```

Open `http://localhost:3000`. The home page calls `GET /health`.

## Run pytest

From the repository root, with the virtualenv active:

```powershell
python -m pytest
```

## Run Ruff

```powershell
python -m ruff check apps/api/src packages/shared/src tests
python -m ruff format apps/api/src packages/shared/src tests
```

## Run MyPy

```powershell
python -m mypy
```

## Alembic

No schema migrations exist in Phase 1 (no domain tables yet). The Alembic environment is wired to `Settings.database_url_sync` and `Base.metadata`:

```powershell
cd apps\api
alembic upgrade head
```

## Makefile

If you have `make` available: `make install`, `make up`, `make test`, `make lint`, `make typecheck`.
