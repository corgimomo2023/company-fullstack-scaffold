from fastapi.testclient import TestClient


def test_project_crud_vertical_slice(client: TestClient) -> None:
    created = client.post(
        "/api/v1/projects",
        json={"name": "Company Portal", "description": "Employee self-service"},
    )
    assert created.status_code == 201
    project = created.json()
    assert project["name"] == "Company Portal"
    assert project["status"] == "active"
    assert project["version"] == 1

    listed = client.get("/api/v1/projects")
    assert listed.status_code == 200
    assert listed.json()["total"] == 1
    assert listed.json()["items"][0]["id"] == project["id"]

    updated = client.patch(
        f"/api/v1/projects/{project['id']}",
        json={"description": "Updated", "version": 1},
    )
    assert updated.status_code == 200
    assert updated.json()["description"] == "Updated"
    assert updated.json()["version"] == 2

    deleted = client.delete(f"/api/v1/projects/{project['id']}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/projects/{project['id']}").status_code == 404


def test_duplicate_name_returns_problem_details(client: TestClient) -> None:
    payload = {"name": "Unique Name", "description": None}
    assert client.post("/api/v1/projects", json=payload).status_code == 201
    response = client.post("/api/v1/projects", json=payload)
    assert response.status_code == 409
    body = response.json()
    assert body["type"] == "https://errors.example.com/conflict"
    assert body["title"] == "Conflict"
    assert body["status"] == 409
    assert body["request_id"]


def test_stale_update_is_rejected(client: TestClient) -> None:
    project = client.post("/api/v1/projects", json={"name": "Versioned"}).json()
    first = client.patch(
        f"/api/v1/projects/{project['id']}", json={"status": "archived", "version": 1}
    )
    assert first.status_code == 200
    stale = client.patch(
        f"/api/v1/projects/{project['id']}", json={"status": "active", "version": 1}
    )
    assert stale.status_code == 409


def test_invalid_name_uses_validation_problem(client: TestClient) -> None:
    response = client.post("/api/v1/projects", json={"name": "  "})
    assert response.status_code == 422
    assert response.json()["title"] == "Validation error"
