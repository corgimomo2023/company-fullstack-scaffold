from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_compose_defaults_to_loopback_only() -> None:
    compose = (ROOT / "compose.yaml").read_text()
    assert '"127.0.0.1:8080:8080"' in compose
    assert '"8080:8080"' not in compose


def test_nginx_security_headers_survive_location_overrides() -> None:
    nginx = (ROOT / "frontend" / "nginx.conf").read_text()
    assert nginx.count("add_header X-Content-Type-Options nosniff always;") == 3
    assert nginx.count("add_header Referrer-Policy strict-origin-when-cross-origin always;") == 3
    assert (
        nginx.count(
            'add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;'
        )
        == 3
    )


def test_ci_exercises_the_production_runtime_and_e2e_flow() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text()
    assert "docker compose up -d --build" in workflow
    assert "docker compose ps --status running" in workflow
    assert "npm run e2e" in workflow
    assert "docker compose logs --no-color" in workflow
    assert "docker compose down -v" in workflow


def test_security_scan_has_a_private_repository_fallback() -> None:
    workflow = (ROOT / ".github" / "workflows" / "codeql.yml").read_text()

    assert "semgrep==1.172.0" in workflow
    assert "semgrep scan" in workflow
    assert "github.event.repository.private == false" in workflow
    assert "github/codeql-action/analyze@v4" in workflow
