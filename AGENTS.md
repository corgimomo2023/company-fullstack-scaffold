# AGENTS.md

## Mission
Maintain a production baseline. Prefer a small verified vertical slice over broad generated boilerplate.

## Required workflow
1. Read this file and the nearest module `AGENTS.md`.
2. For user-facing work, read root `DESIGN.md` before changing layout, color, typography or components.
3. Write or update a failing behavior test before production code.
4. Keep transport, domain, persistence and UI state boundaries explicit.
5. Run the narrow test, then `make check` before handoff.
6. Update migrations, API contract and operations docs when behavior changes.

## Commands
- Setup: `make setup`
- Migrate: `make db-upgrade`
- Development: `make dev`
- All quality gates: `make check`
- Containers: `docker compose up --build`

## Never
- Never hardcode credentials, tokens, internal hosts or personal domains.
- Never use `Base.metadata.create_all()` in production; use Alembic.
- Never let route handlers contain raw SQL or let React components call `fetch` directly.
- Never add a dependency for behavior supported clearly by the platform or existing stack.
- Never claim production readiness from build success alone; exercise health and one real API flow.

## Definition of done
Tests cover success and failure paths; lint/type/test/build pass; migration and rollback implications are reviewed; user-facing states include loading, empty and error; logs contain request IDs without secrets/PII.
