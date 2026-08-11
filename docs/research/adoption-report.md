# Scaffold research and adoption report

Research snapshot: 2026-08-10. GitHub stars are volatile and are used only as an adoption/popularity signal, not a quality score.

## Executive decision

Use a **curated company template**, not a direct clone of a public “full-stack template”. The stack is intentionally smaller than the official FastAPI full-stack template: React/Vite/TypeScript, FastAPI, SQLAlchemy 2 and SQLite, with the engineering controls that make it supportable. The official template is strong evidence for Docker, CI, tests, migrations and generated client patterns, but it targets PostgreSQL/SQLModel and should not be copied blindly.[2]

The scaffold must be a product owned by Platform Engineering: versioned releases, migration notes, dependency updates, quality gates, security review and a measured adoption path. A folder of boilerplate without ownership and upgrade policy will fork into many stale variants.

## Popular projects reviewed

| Project | Stars observed | What was adopted | What was not copied |
|---|---:|---|---|
| FastAPI | 101,462 | typed request/response contracts, dependency injection, OpenAPI, multi-file routers | framework examples are not an application architecture by themselves [1][11] |
| full-stack-fastapi-template | 44,707 | container topology, migrations, CI/E2E mindset | PostgreSQL, SQLModel and built-in auth were outside the fixed stack [2] |
| Vite | 82,285 | official React/TS build foundation and dev proxy | no extra meta-framework or SSR [10] |
| TanStack Query | 50,100 | server-state cache, retries, invalidation and request lifecycle | not used for forms, durable local state or domain logic [4] |
| Playwright | 94,286 | production-entrypoint browser verification across real browser engines | not used as a replacement for fast unit/component tests [5] |
| Bulletproof React | 35,676 | feature-owned frontend modules and explicit shared boundaries | no wholesale folder cargo cult; only the transferable feature-slice rule [6] |
| SQLAlchemy | 12,058 | SQLAlchemy 2 typed models/sessions and portable query layer | no home-grown generic repository framework [3] |
| Cookiecutter | 25,052 | validates demand for repeatable project generation | not adopted as a runtime dependency for this first internal template [7] |
| Copier | 3,518 | future upgrade-aware template option | deferred until the company needs template update propagation and conflict handling [8] |
| AGENTS.md | 23,550 | root and nearest-module instruction layering | no vendor-specific agent as the sole source of truth [9] |

## Required scaffold layers

### 1. Runnable product skeleton

- Real vertical slice with DB migration, typed API, UI states and tests.
- Local development and production-like container topology.
- One command for setup, one for all quality gates, one for migrations.
- Environment schema and safe production defaults.

A skeleton with only `/health` proves almost nothing. The included Projects slice exercises validation, unique conflicts, not-found behavior, optimistic concurrency, list/create UI, persistence and request-ID errors.

### 2. Backend standard

- `API route → service/UoW → focused repository → SQLAlchemy` boundaries; services own commit/rollback and route handlers contain no SQL.
- Pydantic request/response models separate from ORM models.
- Alembic owns production schema history.[13]
- Liveness is dependency-free; readiness probes SQLite.
- A tested online-backup command produces an integrity-checked SQLite copy plus SHA-256 manifest; operators must move both off the application volume and rehearse restore.
- RFC-style problem responses include request IDs.
- Ruff, mypy, pytest and coverage run in CI.

FastAPI's own larger-application guidance demonstrates router/module composition; it does not prescribe adding enterprise abstraction layers.[11] This scaffold therefore avoids premature generic services/base repositories.

### 3. SQLite operating envelope

SQLAlchemy documents SQLite-specific dialect and transaction behaviour; SQLite must be treated as a distinct operational choice, not a miniature PostgreSQL.[12]

Adopted controls:

- foreign keys enabled on every connection;
- WAL mode and a 5-second busy timeout;
- one backend replica;
- persistent volume, tested backups and free-disk alerting;
- version fields for explicit stale-write conflicts;
- documented PostgreSQL migration trigger.

Move to PostgreSQL before horizontal API replicas, sustained concurrent writers, high-availability requirements or backup/maintenance windows exceed the service objective. “FastAPI is async” does not remove SQLite's serialized-write constraint.

### 4. Frontend standard

- Feature folders own API adapter, schema, types, components and tests.
- `App.tsx` only composes shell/routes.
- React Router Data Mode owns route configuration, lazy feature loading and route error boundaries; TanStack Query remains the single owner of server-state caching.[15]
- TanStack Query owns server state; React Hook Form owns form lifecycle; Zod gives immediate client feedback while the backend remains authoritative.[4]
- MSW centralizes integration-test API handlers at the network boundary instead of scattering global `fetch` mocks across tests.[16]
- Every query/mutation has loading, empty, error, success and pending behavior.
- Semantic HTML, visible focus, keyboard behavior and responsive checks are merge gates.
- Vitest/Testing Library cover component behavior; Playwright covers production-entrypoint flows.[5]

Storybook is deliberately deferred until the repository has a genuine shared component/design-system surface. It is valuable for isolated UI development, interaction tests and accessibility addons, but mandatory Storybook for two primitives would add maintenance without protecting another boundary.[17]

The upstream Vite React template evolves quickly and currently favours newer lint tooling. This scaffold keeps ESLint flat config plus typed `typescript-eslint` because its rule/plugin coverage is part of the company quality contract; replacing it with Oxlint/Biome requires a measured rule-gap migration rather than a popularity-driven swap.[10]

### 5. AI-agent context

The repository contains:

- root `AGENTS.md` for invariant commands/boundaries;
- `frontend/AGENTS.md` and `backend/AGENTS.md` for nearest-module rules;
- thin `CLAUDE.md` and `.github/copilot-instructions.md` adapters pointing back to the vendor-neutral rules;
- `.agents/skills/fullstack-feature/SKILL.md` for the repeatable TDD delivery process;
- `.github/prompts/feature.prompt.md` and `review.prompt.md` for outcome/acceptance/risk/evidence structure.

AGENTS.md is an open agent-instruction format with broad repository adoption.[9] GitHub also supports repository custom instruction files, so the adapter is included without making Copilot the source of truth.[14]

### 6. Governance and lifecycle

Required controls included in this artifact:

- CODEOWNERS, PR and issue templates;
- branch/required-review policy to configure in the hosting platform;
- CI gates for formatting, lint, types, tests, coverage, build, generator and containers;
- Dependabot configuration and lock files;
- `SECURITY.md`, data/logging rules and explicit “no fake auth” boundary;
- architecture decisions, operations runbook, migration and rollback expectations.

The missing organizational inputs must be decided before promotion: real GitHub teams in CODEOWNERS, identity provider, authorization model, data classification, release owner, support SLOs, secret manager, ingress/TLS and backup retention.

## Generator choice

The included `scripts/create_project.py` is dependency-free, deterministic and tested. It is enough for initial standardisation because it copies one curated source and performs constrained identifier replacement.

Upgrade to Copier when Platform Engineering commits to propagating template updates into existing generated repositories; Copier is designed around rendering project templates and is a better fit for update-aware evolution than a one-time copy.[8] Cookiecutter remains a mature one-time generation option but does not by itself solve fleet upgrades.[7]

## Rollout recommendation

1. Pilot with 2 real internal services, not toy demos.
2. Measure setup time, CI pass rate, exceptions requested and production incidents.
3. Fix the template centrally; do not let pilot teams fork conventions silently.
4. Tag scaffold releases and publish migration notes.
5. Add approved SSO/authorization and observability adapters only after the company standards are known.
6. Reassess SQLite after real write-concurrency and availability data, not preference.

## Rejected shortcuts

- A monolithic `App.tsx` or FastAPI `main.py` containing feature logic.
- `create_all()` in production instead of Alembic.
- wildcard production CORS.
- fake JWT/password auth included for appearances.
- “async everywhere” despite SQLite's write model.
- copying a high-star template without a documented delta.
- agent prompts without executable verification commands.
- claiming production readiness from generated files or a successful compile alone.

## Sources

[1] https://github.com/fastapi/fastapi
[2] https://github.com/fastapi/full-stack-fastapi-template
[3] https://github.com/sqlalchemy/sqlalchemy
[4] https://github.com/TanStack/query
[5] https://github.com/microsoft/playwright
[6] https://github.com/alan2207/bulletproof-react
[7] https://github.com/cookiecutter/cookiecutter
[8] https://github.com/copier-org/copier
[9] https://github.com/agentsmd/agents.md
[10] https://github.com/vitejs/vite
[11] https://fastapi.tiangolo.com/tutorial/bigger-applications
[12] https://docs.sqlalchemy.org/en/20/dialects/sqlite.html
[13] https://alembic.sqlalchemy.org/en/latest/tutorial.html
[14] https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot
[15] https://github.com/remix-run/react-router
[16] https://github.com/mswjs/msw
[17] https://github.com/storybookjs/storybook
