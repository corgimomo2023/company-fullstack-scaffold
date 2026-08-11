# Architecture decisions

## Monorepo and feature slices
Frontend and backend share one review unit while keeping independent dependency/build boundaries. Features own their UI, hooks, schemas and API adapter; backend routes adapt HTTP, services own use-case transactions, and focused repositories own persistence expressions without commit/rollback.

## Synchronous SQLAlchemy with SQLite
SQLite serializes writes. The API uses ordinary SQLAlchemy 2 sessions, WAL, foreign keys and a five-second busy timeout. This is simpler than introducing an async driver without gaining write parallelism.

## Migrations
Development tests may create an isolated schema for speed. Production sets `APP_AUTO_CREATE_SCHEMA=false`; `start.sh` applies Alembic migrations before Uvicorn.

## Concurrency
Project updates carry a version. Stale writes return `409`, making lost-update behavior explicit. For higher write concurrency, replicas, background workers or high availability, migrate the SQLAlchemy URL and migration compatibility to PostgreSQL.

## Security
No insecure default identity exists. Deployment is private until company SSO and server-side authorization are integrated. CORS/trusted hosts are explicit, containers are non-root and errors/logs avoid implementation details.

## Frontend runtime and testing
React Router Data Mode owns route topology, lazy feature loading and route-level failures. TanStack Query owns server-state caching and does not duplicate router loading. Vitest/Testing Library tests observable UI behaviour, while MSW owns test API interception centrally. Storybook remains optional until shared UI components justify a maintained component workbench.
