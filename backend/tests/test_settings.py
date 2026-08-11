import pytest
from pydantic import ValidationError

from app.config import Settings


def test_production_rejects_wildcard_cors() -> None:
    with pytest.raises(ValidationError):
        Settings(environment="production", cors_origins=["*"])
