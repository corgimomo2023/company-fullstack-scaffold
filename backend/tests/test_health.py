from fastapi.testclient import TestClient


def test_liveness_does_not_depend_on_database(client: TestClient) -> None:
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_checks_database(client: TestClient) -> None:
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready", "database": "ok"}


def test_api_documentation_is_reachable_through_nginx_api_prefix(client: TestClient) -> None:
    assert client.get("/api/docs").status_code == 200
    assert client.get("/api/openapi.json").status_code == 200
    assert client.get("/docs").status_code == 404
