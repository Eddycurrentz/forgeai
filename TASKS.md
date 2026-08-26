# TASKS.md

Phased delivery for ForgeAI. **Phase 1 is in progress / implemented as foundation.** Later phases must not start until the previous phase’s acceptance criteria pass.

---

## Phase 1 — Project foundation

**Objective:** Runnable monorepo with FastAPI health, Next.js shell, Postgres, Redis, Settings, SQLAlchemy, Alembic, pytest, Ruff, MyPy, and Compose.

**Files:** `apps/api/**`, `apps/web/**`, `packages/shared/**`, `docker-compose.yml`, `Makefile`, `.env.example`, `pyproject.toml`, `tests/**`, root docs.

**Dependencies:** None.

**Tests:** `tests/test_config.py`, `tests/test_health.py`.

**Acceptance criteria:**

- `GET /health` returns JSON with `status`, `postgres`, `redis`, `version`.
- Compose starts `api`, `web`, `postgres`, `redis`.
- Settings load from `.env`.
- Alembic is configured against `Base.metadata`.
- pytest, Ruff, and MyPy run from the repo root.
- No LangGraph, RAG, sandbox, or Git automation code.

---

## Phase 2 — Persistence schema

**Objective:** Alembic migrations for repositories, runs, jobs, and approvals.

**Files:** `apps/api/src/forgeai_api/models/`, `apps/api/alembic/versions/`, `packages/shared` types.

**Dependencies:** Phase 1.

**Tests:** Migration upgrade/downgrade; model round-trip against Postgres.

**Acceptance criteria:** `alembic upgrade head` creates real tables; no dummy columns; foreign keys and timestamps present.

---

## Phase 3 — API run lifecycle and workers

**Objective:** Create/list runs as durable jobs; Redis-backed worker process.

**Files:** `apps/api/src/forgeai_api/api/runs.py`, worker module, Redis queue helpers.

**Dependencies:** Phase 2.

**Tests:** Run create/get; worker picks a job (integration with Redis).

**Acceptance criteria:** A run record moves `queued → running → succeeded|failed` without any LLM calls.

---

## Phase 4 — Git workspace ingest

**Objective:** Clone/fetch a repository into an isolated workdir and expose the file tree.

**Files:** `packages/git/`, API ingest endpoints.

**Dependencies:** Phase 3.

**Tests:** Clone a fixture repo; reject paths outside the workdir.

**Acceptance criteria:** Ingest stores commit SHA and tree listing; no commit/push automation yet.

---

## Phase 5 — Tree-sitter indexing

**Objective:** Parse supported languages into AST-backed chunks and a symbol table.

**Files:** `packages/code-intelligence/`.

**Dependencies:** Phase 4.

**Tests:** Fixture sources produce stable chunk IDs and symbol names.

**Acceptance criteria:** Index is persisted; no embeddings yet.

---

## Phase 6 — Embeddings and agentic RAG

**Objective:** Embed chunks into pgvector; retrieve with citations.

**Files:** `packages/rag/`, pgvector migration, LLM embed adapter in `packages/llm`.

**Dependencies:** Phase 5.

**Tests:** Retrieval returns cited chunk IDs for a known query fixture.

**Acceptance criteria:** Query API returns snippets + paths; no generation of patches.

---

## Phase 7 — LangGraph planning

**Objective:** Planner graph with Postgres checkpointer; no file writes.

**Files:** `packages/agent/`, graph definition, run adapter.

**Dependencies:** Phase 3, Phase 6.

**Tests:** Graph produces a structured plan from retrieved context (recorded fixtures).

**Acceptance criteria:** Plan is stored on the run; interrupts are defined for later HITL.

---

## Phase 8 — Code search and repository understanding

**Objective:** Tools for search, read, outline, and dependency map used by the graph.

**Files:** `packages/code-intelligence/` tools, agent tool bindings.

**Dependencies:** Phase 5, Phase 7.

**Tests:** Search returns known symbols from fixtures.

**Acceptance criteria:** Tools are read-only.

---

## Phase 9 — Code modification and human approval

**Objective:** Produce unified diffs; apply only after approval.

**Files:** patch service, approval API, web approval UI.

**Dependencies:** Phase 8.

**Tests:** Apply/rollback on a fixture; unapproved apply is rejected.

**Acceptance criteria:** LangGraph interrupt before write; audit row in `approvals`.

---

## Phase 10 — Docker sandbox and test execution

**Objective:** Run project tests in an ephemeral container with resource limits.

**Files:** `packages/execution/`, sandbox image under `infrastructure/`.

**Dependencies:** Phase 9.

**Tests:** Fixture project tests run in-container; timeout/OOM handled.

**Acceptance criteria:** Host filesystem outside the workspace is not writable from the sandbox.

---

## Phase 11 — Autonomous debugging

**Objective:** Bounded fail-test loop that edits, re-runs tests, and stores an evidence pack.

**Files:** `packages/agent/` debug subgraph.

**Dependencies:** Phase 10.

**Tests:** Seeded failing test is fixed within N iterations on a fixture, or run fails closed.

**Acceptance criteria:** Max iterations enforced; no infinite loops.

---

## Phase 12 — Code review and security review

**Objective:** Review agents emit structured findings (quality + security), not exploits.

**Files:** review prompts/tools, findings schema.

**Dependencies:** Phase 9.

**Tests:** Known-bad fixture yields expected finding codes.

**Acceptance criteria:** Output is SARIF-like findings; no payload generation.

---

## Phase 13 — Git integration

**Objective:** Create a branch, commit approved patches, optionally open a PR (GitHub later).

**Files:** `packages/git/` write path, API.

**Dependencies:** Phase 9, Phase 12.

**Tests:** Commit on fixture repo; dirty tree rejected without approval.

**Acceptance criteria:** Authored commits are traceable to a run ID.

---

## Phase 14 — Observability

**Objective:** OpenTelemetry traces/metrics for runs, tools, model calls, sandbox jobs.

**Files:** tracing middleware, run timeline API.

**Dependencies:** Phase 3+.

**Tests:** A run produces a trace with tool spans.

**Acceptance criteria:** Timeline API returns ordered events for a run.

---

## Phase 15 — Evaluation and operator UI

**Objective:** Golden-task harness plus Next.js console for runs, approvals, and logs.

**Files:** `packages/evaluation/`, `apps/web` run/approval views.

**Dependencies:** Phases 7–14 as features land; UI can iterate after Phase 3.

**Tests:** Eval suite fails the build if a golden task regresses; UI Playwright smoke for health + run list.

**Acceptance criteria:** `evals/` can run headlessly; console can approve a waiting run in a local demo.
