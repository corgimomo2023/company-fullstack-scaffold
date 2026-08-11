# Roadmap alignment

This repository is the first golden-path scaffold in a broader governed AI-assisted delivery platform. It is not the complete company platform.

## Delivered in this repository

- Versioned React/Vite + FastAPI/SQLAlchemy/Alembic generator with provenance and generated lock-file consistency checks.
- Reproducible Dev Container, pinned Node/npm, Python locks and one-command setup/check workflow.
- Complete CRUD vertical slice with API errors, service-owned transactions, repository persistence and atomic optimistic concurrency.
- SQLite foreign keys, WAL, busy timeout, migrations, online backup, integrity verification and restore guidance.
- Vendor-neutral `AGENTS.md`, module instructions, focused prompts and a reusable full-stack feature skill.
- CI for lint, type checking, tests, migration checks, dependency audit, production container startup, readiness, security headers and Playwright E2E.
- CODEOWNERS, issue/PR templates, Dependabot, CodeQL, security policy and operations runbook.

## Deliberate pilot differences

The roadmap describes the target platform, while this repository follows the approved scaffold constraints used for the first implementation:

| Area | Current scaffold | Roadmap target | Follow-up decision |
|---|---|---|---|
| Python | 3.11 baseline | 3.13 | Upgrade only after company runtime/image compatibility validation. |
| Frontend package manager | npm 10 with lockfile | pinned pnpm | Select one organization standard, then migrate generator and CI atomically. |
| Database | SQLite reference runtime | SQLite local; PostgreSQL hosted | Add a PostgreSQL integration-test/hosted profile before multi-instance or high-write workloads. |
| Agent adapter | Vendor-neutral rules plus Copilot/Claude adapters | Cline pilot | Add thin `.clinerules/` and `.cline/skills/` adapters without duplicating the canonical rules. |
| Deployment | Local production-container topology | preview/staging/production platform | Keep deployment-provider concerns outside the scaffold until the scored platform spike selects a target. |

These differences must not be hidden by changing generated projects independently. Each organization-wide change requires a template version, migration note, regenerated example and CI verification.

## Next roadmap gates

### Complete M1

1. Validate the Dev Container on company-managed Windows and macOS.
2. Add PostgreSQL Compose/testing profile and run the same repository/service tests against it.
3. Add the first five Cline skill adapters and a versioned 20–50 task evaluation baseline.
4. Measure median clone-to-working-app time and setup success with pilot users.

### Build M2 outside this application repository

1. Move common CI into organization-owned reusable workflows and enforce repository rulesets.
2. Add secret scanning, dependency review, container/IaC scanning, SBOM and license policy.
3. Build immutable images once and promote the same digest through preview, staging and production.
4. Select a deployment target through the managed-PaaS versus Coolify spike.
5. Use GitHub OIDC and protected environments; do not introduce long-lived deployment keys.
6. Demonstrate preview expiry, rollback and restore in a game day.

### Platform boundary

The future portal, AI gateway, skill registry, preview controller, cost/health catalog and deployment control plane are separate products. They should consume this scaffold's metadata and contracts rather than being embedded in every generated application.
