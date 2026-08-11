---
applyTo: "backend/**/*.py,backend/**/*.ini,backend/**/*.toml"
---
Follow `backend/AGENTS.md`. Preserve the router → service/UoW → focused repository boundary. Repositories flush persistence changes but never commit or roll back. Every schema change needs an reviewed Alembic migration and migration test.
