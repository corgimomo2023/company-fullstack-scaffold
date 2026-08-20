import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "create_project.py"
TEMPLATE_SMOKE_WORKFLOW = (
    Path(__file__).parents[1] / ".github" / "workflows" / "template-smoke-test.yml"
)


def load_generator():
    spec = importlib.util.spec_from_file_location("create_project", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generator_creates_customized_project(tmp_path: Path) -> None:
    module = load_generator()
    destination = tmp_path / "asset-register"
    module.generate(
        destination,
        slug="asset-register",
        display_name="Asset Register",
        codeowner="@acme/platform-team",
    )
    assert (destination / "frontend" / "package.json").is_file()
    assert (destination / "backend" / "pyproject.toml").is_file()
    assert "Asset Register" in (destination / "README.md").read_text()
    assert "company-fullstack-scaffold" not in (destination / "README.md").read_text()
    assert "@acme/platform-team" in (destination / ".github" / "CODEOWNERS").read_text()
    assert "@platform-team" not in (destination / ".github" / "CODEOWNERS").read_text()
    metadata = (destination / ".scaffold.json").read_text()
    assert '"template_version": "1.0.0"' in metadata
    assert '"slug": "asset-register"' in metadata
    assert "company-app-api" not in (destination / "backend" / "uv.lock").read_text()
    assert "asset-register-api" in (destination / "backend" / "uv.lock").read_text()
    assert (
        "company-app-web"
        not in (destination / "frontend" / "package-lock.json").read_text()
    )
    assert (
        "asset-register-web"
        in (destination / "frontend" / "package-lock.json").read_text()
    )
    assert not (destination / "node_modules").exists()
    assert not (destination / ".venv").exists()
    assert not list(destination.rglob("*.tsbuildinfo"))
    assert not (destination / "scripts" / "create_project.py").exists()
    assert not (destination / "tests" / "test_scaffold.py").exists()
    assert not (destination / "scaffold.yaml").exists()
    assert not (destination / "TEMPLATE_VERSION").exists()
    assert not (
        destination / ".github" / "workflows" / "template-smoke-test.yml"
    ).exists()
    assert "## Create a project" not in (destination / "README.md").read_text()
    assert (
        "generator:"
        not in (destination / ".github" / "workflows" / "ci.yml").read_text()
    )
    pen_check = subprocess.run(
        [
            sys.executable,
            str(destination / "scripts" / "export_pen_design_system.py"),
            "--check",
        ],
        cwd=destination,
        capture_output=True,
        text=True,
        check=False,
    )
    assert pen_check.returncode == 0, pen_check.stdout + pen_check.stderr


def test_generator_rejects_unsafe_slug(tmp_path: Path) -> None:
    module = load_generator()
    with pytest.raises(ValueError, match="lowercase kebab-case"):
        module.generate(
            tmp_path / "bad",
            slug="../bad",
            display_name="Bad",
            codeowner="@acme/platform-team",
        )


def test_generated_project_smoke_installs_playwright_before_check() -> None:
    workflow = TEMPLATE_SMOKE_WORKFLOW.read_text()
    setup = workflow.index("run: make setup")
    install = workflow.index("npx playwright install --with-deps chromium")
    check = workflow.index("run: make check")

    assert setup < install < check
