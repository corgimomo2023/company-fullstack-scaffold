from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.database import reset_engine
from app.main import create_app


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    db_path = tmp_path / "test.db"
    settings = Settings(
        environment="test",
        database_url=f"sqlite:///{db_path}",
        cors_origins=["http://localhost:5173"],
    )
    reset_engine()
    app = create_app(settings)
    app.dependency_overrides[get_settings] = lambda: settings
    with TestClient(app) as test_client:
        yield test_client
    reset_engine()
