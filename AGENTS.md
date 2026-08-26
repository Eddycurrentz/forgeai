# AGENTS.md

Operating rules for humans and coding agents working in ForgeAI.

## Mission

Build an industrial autonomous software engineer **one phase at a time**. Phase 1 is foundation only. Do not implement later phases unless the current task explicitly names them.

## Out of scope until their phase

- LangGraph / agent graphs
- Embeddings, RAG, pgvector indexes
- Tree-sitter indexing and code search
- Docker sandboxing and test execution
- Git clone/commit/PR automation
- Placeholder LLM replies or fake “agent” JSON

If a request would add those capabilities during Phase 1, refuse and point at [TASKS.md](TASKS.md).

## Repository conventions

- Domain logic belongs in `packages/*`. The HTTP surface lives in `apps/api`. The operator UI lives in `apps/web`.
- Empty packages (`agent`, `rag`, `code-intelligence`, `execution`, `git`, `llm`, `evaluation`) stay documentation-only until their phase.
- Configuration is `pydantic-settings` in `forgeai_api.core.config`. Do not scatter `os.getenv` calls.
- Database access goes through SQLAlchemy 2.x (`forgeai_api.core.db`). Schema changes go through Alembic.
- Redis access goes through `forgeai_api.core.redis`.
- Secrets stay in `.env`. Commit `.env.example` only.

## Python

- Python 3.12+, type-annotated, Ruff + MyPy clean.
- FastAPI routers are thin. Put side effects in core modules or packages.
- Prefer explicit failures over silent defaults for infrastructure URLs.
- Tests live in `tests/` and must not require a live Postgres/Redis for unit tests. Mock I/O at the ping/client boundary.

## TypeScript

- Strict TypeScript in `apps/web`.
- Server Components by default. Do not add a global client store in Phase 1.
- `NEXT_PUBLIC_API_URL` is the only frontend config for now.

## Quality bar

Before finishing a change:

1. `python -m pytest`
2. `python -m ruff check apps/api/src packages/shared/src tests`
3. `python -m mypy`

Do not add dependencies unless Phase 1 (or the named later phase) needs them.

## Git

Do not commit `.env`, credentials, or generated `node_modules` / `.venv`. Do not invent Git history or force-push.
