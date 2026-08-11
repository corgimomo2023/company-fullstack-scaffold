#!/usr/bin/env python3
import argparse
import json
import re
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]
SKIP_NAMES = {
    ".git",
    ".venv",
    "node_modules",
    "dist",
    "coverage",
    "htmlcov",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "examples",
}
TEXT_SUFFIXES = {
    "",
    ".md",
    ".txt",
    ".toml",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".css",
    ".html",
    ".sh",
    ".ini",
    ".example",
    ".lock",
}


def generate(destination: Path, *, slug: str, display_name: str, codeowner: str) -> None:
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", slug):
        raise ValueError("slug must be lowercase kebab-case")
    if not display_name.strip():
        raise ValueError("display name is required")
    if not re.fullmatch(r"@[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)?", codeowner):
        raise ValueError("codeowner must be a GitHub user or team such as @org/platform-team")

    destination = destination.resolve()
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")
    if SOURCE == destination or SOURCE in destination.parents:
        raise ValueError("destination must be outside the scaffold source")

    snake = slug.replace("-", "_")
    replacements = {
        "Company Full-Stack Scaffold": display_name,
        "Company Application": display_name,
        "company-fullstack-scaffold": slug,
        "company-app": slug,
        "company_app": snake,
        "@corgimomo2023": codeowner,
        "@platform-team": codeowner,
        "@frontend-team": codeowner,
        "@backend-team": codeowner,
        "@security-team": codeowner,
    }

    def ignore(_path: str, names: list[str]) -> set[str]:
        return {
            name
            for name in names
            if name in SKIP_NAMES
            or name.endswith(".egg-info")
            or name.endswith(".tsbuildinfo")
            or name == ".env"
        }

    shutil.copytree(SOURCE, destination, ignore=ignore)
    for path in destination.rglob("*"):
        if (
            not path.is_file()
            or path.suffix not in TEXT_SUFFIXES
            or path.name == "citations.json"
        ):
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text)

    version = (SOURCE / "TEMPLATE_VERSION").read_text().strip()
    generated_only_files = [
        "scripts/create_project.py",
        "tests/test_scaffold.py",
        "scaffold.yaml",
        "TEMPLATE_VERSION",
        ".github/workflows/template-smoke-test.yml",
    ]
    for relative_path in generated_only_files:
        (destination / relative_path).unlink(missing_ok=True)

    readme = destination / "README.md"
    readme_text = readme.read_text()
    start = readme_text.index("## Create a project")
    end = readme_text.index("## Quality contract")
    readme.write_text(readme_text[:start] + readme_text[end:])

    ci_workflow = destination / ".github" / "workflows" / "ci.yml"
    ci_text = ci_workflow.read_text()
    generator_start = ci_text.index("  generator:\n")
    containers_start = ci_text.index("  containers:\n")
    ci_workflow.write_text(ci_text[:generator_start] + ci_text[containers_start:])

    for relative_dir in ("scripts", "tests"):
        directory = destination / relative_dir
        if directory.exists() and not any(directory.iterdir()):
            directory.rmdir()

    metadata = {
        "template": "company-fullstack-scaffold",
        "template_version": version,
        "slug": slug,
        "display_name": display_name,
        "codeowner": codeowner,
    }
    (destination / ".scaffold.json").write_text(json.dumps(metadata, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a project from the company full-stack scaffold"
    )
    parser.add_argument("destination", type=Path)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--codeowner", required=True)
    args = parser.parse_args()
    generate(
        args.destination,
        slug=args.slug,
        display_name=args.display_name,
        codeowner=args.codeowner,
    )
    print(f"Created {args.display_name} at {args.destination.resolve()}")


if __name__ == "__main__":
    main()
