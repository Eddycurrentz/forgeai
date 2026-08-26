# DECISIONS.md

Architecture decision records for ForgeAI. Date: 2026-08-26.

## ADR-001: Monorepo

**Decision:** One repository with `apps/*` and `packages/*`.

**Why:** The API, web console, and domain libraries will share types and evolve together. A monorepo keeps Phase 1 small while leaving package boundaries obvious.

**Consequences:** Root `pyproject.toml` holds Ruff/MyPy/pytest. Each installable Python package has its own `pyproject.toml`.

## ADR-002: FastAPI + Next.js

**Decision:** Python 3.12 FastAPI for the control plane; Next.js + TypeScript + Tailwind for the operator UI.

**Why:** FastAPI fits typed settings, OpenAPI, and async Postgres/Redis. Next.js is the requested UI stack.

## ADR-003: PostgreSQL and Redis from day one

**Decision:** Run both in Compose in Phase 1, even before domain tables or queues exist.

**Why:** Health, Alembic, and later LangGraph checkpoints/RAG all assume these processes. Wiring them now avoids a fake in-memory foundation.

## ADR-004: SQLAlchemy 2.x + Alembic, no tables yet

**Decision:** Ship engine, session factory, `DeclarativeBase`, and Alembic `env.py`. Do not invent placeholder tables.

**Why:** Empty metadata is honest. The first real models appear when runs/repos exist (Phase 2).

## ADR-005: Dual Postgres URLs

**Decision:** `DATABASE_URL` uses `postgresql+asyncpg` (API). `DATABASE_URL_SYNC` uses `postgresql+psycopg` (Alembic).

**Why:** Alembic’s default runner is synchronous. The API is async.

## ADR-006: Pydantic Settings

**Decision:** All runtime config goes through `forgeai_api.core.config.Settings`.

**Why:** Typed, documented, `.env`-aware, and testable without patching `os.environ` everywhere.

## ADR-007: Defer LangGraph, RAG, sandbox, Git

**Decision:** Phase 1 does not import LangGraph, embedding clients, Tree-sitter, Docker SDK, or GitPython.

**Why:** Those systems are high-cost and undefined until retrieval, tools, and HITL exist. Empty package READMEs reserve names without fake APIs.

## ADR-008: Health reports dependency truth

**Decision:** `/health` always returns HTTP 200 with `status: ok | degraded` and boolean `postgres` / `redis` fields.

**Why:** Process liveness stays true if a dependency is down; operators still see which probe failed. Unit tests mock pings so CI does not need Docker.

## ADR-009: pgvector image deferred

**Decision:** Phase 1 uses `postgres:16-alpine`. Switch to a pgvector image when embeddings land.

**Why:** No vector extension is used yet. A plain Postgres image is smaller and sufficient for `SELECT 1`.

## ADR-010: License

**Decision:** Package metadata uses Apache-2.0 until a product owner chooses otherwise.
