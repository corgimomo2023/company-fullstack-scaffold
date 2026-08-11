# Backend agent instructions

- HTTP adapters stay in `app/api/`; services own use-case rules plus commit/rollback; repositories only query/flush persistence. Pydantic schemas are API contracts, not ORM models.
- Use SQLAlchemy 2 typed mappings and parameterized expressions. Commit/rollback ownership is explicit.
- Every schema change requires an Alembic migration. Test migrations against a fresh database and an upgrade path.
- Return RFC 9457-style problem details with a request ID; do not leak stack traces, SQL, secrets or PII.
- Keep liveness dependency-free. Readiness may probe required dependencies.
- SQLite requires foreign keys, WAL, busy timeout, durable backups and one API replica.
- Tests: `.venv/bin/pytest`; full gate: `.venv/bin/ruff format --check . && .venv/bin/ruff check . && .venv/bin/mypy app && .venv/bin/pytest --cov=app`.
