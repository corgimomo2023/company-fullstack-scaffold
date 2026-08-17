SHELL := /bin/bash
.PHONY: setup dev check backend-check frontend-check design-check db-upgrade compose-check
setup:
	python3 -m venv backend/.venv
	cd backend && .venv/bin/pip install -r requirements-dev.lock
	backend/.venv/bin/pip install -r requirements-design.txt
	cd frontend && npm ci

lock:
	uv lock --project backend
	uv export --project backend --no-dev --no-hashes --no-editable --output-file backend/requirements.lock
	uv export --project backend --extra dev --no-hashes --output-file backend/requirements-dev.lock
	cd frontend && npm install --package-lock-only

dev:
	@trap 'kill 0' EXIT; backend/.venv/bin/uvicorn app.main:app --app-dir backend --reload & cd frontend && npm run dev

backend-check:
	cd backend && .venv/bin/ruff format --check . && .venv/bin/ruff check . && .venv/bin/mypy app && .venv/bin/pytest --cov=app --cov-report=term-missing

frontend-check:
	cd frontend && npm run lint && npm run typecheck && npm test && npm run build

design-check:
	backend/.venv/bin/ruff format --check scripts/audit_aai_design_system.py scripts/export_design_system.py tests/test_design_system.py tests/test_common_look_and_feel.py
	backend/.venv/bin/ruff check scripts/audit_aai_design_system.py scripts/export_design_system.py tests/test_design_system.py tests/test_common_look_and_feel.py
	npx -y @google/design.md@0.4.0 lint DESIGN.md
	npx -y html-validate@10.4.0 .agents/skills/common-look-and-feel/templates/admin-cms.html
	backend/.venv/bin/python scripts/export_design_system.py --check
	backend/.venv/bin/pytest tests/test_design_system.py tests/test_common_look_and_feel.py -q

check: backend-check frontend-check design-check
	backend/.venv/bin/pytest tests -q

db-upgrade:
	cd backend && .venv/bin/alembic upgrade head

compose-check:
	docker compose config --quiet
