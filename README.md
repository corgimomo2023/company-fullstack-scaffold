# Company Full-Stack Scaffold

## Design system

The machine-readable company visual baseline is defined in [`DESIGN.md`](DESIGN.md). It was derived from the public Asia Allied Infrastructure website for internal admin, CMS and operational applications, with accessibility corrections documented in the file.

Coding agents must read `DESIGN.md` before changing colors, typography, layout or component styling. The extracted baseline is not a substitute for an official internal corporate brand manual.

Production baseline for company applications using a React/Vite SPA, FastAPI, SQLAlchemy 2 and SQLite. The included **Projects** feature is a complete vertical slice, not sample-only architecture: validation, API error contracts, persistence, optimistic concurrency, tests and responsive UI all use the same boundaries expected of new features.

## Quick start

Prerequisites: Python 3.11+, Node `>=22.12 <23`, npm 10, Docker Compose and `make`. Use `frontend/.node-version` rather than an arbitrary Node runtime.

```bash
cp .env.example .env
make setup
make db-upgrade
make dev
```

Or run the production container topology. Compose binds to loopback by default because this scaffold has no authentication; expose it only through an approved TLS/authenticated ingress:

```bash
docker compose up --build
# UI: http://localhost:8080
# API docs: http://localhost:8080/api/docs (disabled/restricted at the edge if required)
```

## Create a project

```bash
python3 scripts/create_project.py ../asset-register \
  --slug asset-register \
  --display-name "Asset Register" \
  --codeowner @your-org/platform-team
cd ../asset-register && make setup && make check
```

## Quality contract

`make check` runs backend Ruff, mypy and pytest plus frontend ESLint, TypeScript, Vitest, production build and scaffold/runtime contract tests. CI also starts the production containers, waits for readiness, checks security headers and runs the Playwright critical path. Do not merge generated code that cannot pass these gates.

Dependency changes must refresh and review both lock formats with `make lock` (requires `uv` for Python and npm for frontend). Production images install from the committed Python lock export; frontend uses `npm ci`.

## Structure

- `frontend/src/features/`: feature-owned React modules; shared primitives stay in `components/` and transport in `lib/`.
- `backend/app/api/`: HTTP adapters; services own business rules/transactions; repositories own SQLAlchemy persistence only.
- `backend/alembic/`: schema history; production startup applies migrations.
- `AGENTS.md`, module `AGENTS.md`, `.github/copilot-instructions.md`, `CLAUDE.md`: layered agent context.
- `.agents/skills/fullstack-feature/SKILL.md`: reusable delivery procedure.
- `.github/prompts/`: task prompts with explicit acceptance/verification fields.
- `docs/`: architecture decisions, operations, research and plans.

## Deliberate boundaries

- SQLite is appropriate for one application instance and modest write concurrency. WAL and a busy timeout are enabled. Move to PostgreSQL before horizontal API scaling or sustained concurrent writes.
- Authentication is intentionally **not faked**. Integrate the company identity provider and authorization policy before public exposure; see `SECURITY.md`.
- The backend is synchronous because SQLite serializes writes; async syntax would not create write concurrency.
- Domain code must not import FastAPI request/response objects.

See `docs/research/adoption-report.md`, `docs/strategy/platform-roadmap.md`, `docs/architecture/decisions.md`, and `docs/operations/runbook.md`.
