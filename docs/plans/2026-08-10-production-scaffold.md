# Company Full-Stack Scaffold Implementation Plan

> **For Hermes:** Use test-driven-development discipline and verify each vertical slice before completion.

**Goal:** Build a reusable, production-grade company scaffold and a generated example using React/Vite/TypeScript, FastAPI/Python/SQLAlchemy 2, and SQLite.

**Architecture:** A monorepo template with independently testable frontend and backend, a real `projects` CRUD vertical slice, versioned Alembic migrations, SQLite production pragmas, container deployment, CI quality gates, layered AI-agent instructions, and a dependency-free project generator. The template itself remains runnable; `example/` proves generation works.

**Tech Stack:** Vite, React, TypeScript, React Router, TanStack Query, React Hook Form, Zod, Vitest, Testing Library, Playwright; FastAPI, SQLAlchemy 2, Alembic, Pydantic Settings, pytest, Ruff, mypy; Docker Compose, Nginx, GitHub Actions.

---

## Task 1: Repository and governance shell

**Files:** root `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODEOWNERS`, `.editorconfig`, `.gitignore`, `.env.example`, `Makefile`, `.github/*`, `docs/*`.

1. Define supported workflow, ownership, security boundaries and quality gates.
2. Add layered agent instructions and vendor-neutral prompt templates.
3. Add a reusable in-repo `SKILL.md` for delivering features safely.
4. Verify all referenced commands map to real scripts or Make targets.

## Task 2: Backend vertical slice (TDD)

**Tests first:** `backend/tests/test_health.py`, `backend/tests/test_projects_api.py`, `backend/tests/test_settings.py`.

1. Write tests for liveness/readiness, project CRUD/conflict/not-found, validation and settings.
2. Run pytest and verify expected import/feature failures.
3. Implement config, database/session lifecycle, models, schemas, repository, service, routers, structured request logging and error contracts.
4. Add Alembic baseline migration and SQLite WAL/foreign-key/busy-timeout pragmas.
5. Run pytest, Ruff and mypy until clean.

## Task 3: Frontend vertical slice (TDD)

**Tests first:** `frontend/src/features/projects/*.test.tsx`, `frontend/src/lib/api.test.ts`.

1. Write tests for project list states, create validation, API problem parsing and route shell.
2. Run Vitest and verify expected missing-module failures.
3. Implement query client, typed API boundary, routes, accessible UI primitives and feature modules.
4. Run Vitest, ESLint, TypeScript and production build until clean.

## Task 4: Deployment and generator

**Files:** backend/frontend Dockerfiles, `frontend/nginx.conf`, `compose.yaml`, `scripts/create-project.py`, `scaffold.yaml`, `example/`.

1. Add non-root containers, health checks, immutable frontend assets, SPA fallback and `/api` reverse proxy.
2. Add SQLite named volume and explicit environment configuration.
3. Build a dependency-free generator that validates project identifiers, copies the template and replaces safe tokens.
4. Generate `example/` and prove its source tree contains no unresolved scaffold tokens.

## Task 5: Quality and operational verification

1. Install locked dependencies.
2. Run backend tests with coverage, Ruff format/check and mypy.
3. Run frontend tests, lint, typecheck and build.
4. Run generator tests and scan for secrets/debug placeholders.
5. Validate Docker Compose config; build and start containers if Docker is available.
6. Probe liveness, readiness, CRUD API and SPA through the container entrypoint.
7. Request independent code review and fix blocking findings.

## Task 6: Research report

**Files:** `docs/research/adoption-report.md`, `docs/architecture/decisions.md`, `docs/operations/runbook.md`.

1. Record current source metadata and direct links for official/popular projects.
2. Separate adopted, optional and rejected patterns.
3. Explain SQLite operating envelope and PostgreSQL migration path.
4. Verify citations and ensure README links to the report.

## Acceptance Criteria

- Fresh clone can run `make setup`, `make check`, and `docker compose up --build`.
- The project CRUD slice is persisted through SQLAlchemy and Alembic-managed SQLite.
- API and UI tests cover success, loading/empty/error, validation, conflict and missing-resource paths.
- CI blocks formatting, lint, type, test and build regressions.
- Root and module `AGENTS.md`, prompt templates and reusable skill provide precise commands and boundaries.
- `scripts/create-project.py` creates a separately runnable project without unresolved placeholders.
- No hardcoded secrets, personal domains or machine-specific absolute paths are present in the reusable artifact.
