from pathlib import Path

import pytest
from sqlalchemy.orm import Session

from app.config import Settings
from app.database import create_database_engine
from app.errors import DomainError
from app.models import Base
from app.schemas import ProjectCreate, ProjectUpdate
from app.services import ProjectService


def test_concurrent_update_uses_atomic_version_predicate(tmp_path: Path) -> None:
    settings = Settings(environment="test", database_url=f"sqlite:///{tmp_path / 'race.db'}")
    engine = create_database_engine(settings)
    Base.metadata.create_all(engine)

    with Session(engine) as setup_session:
        project = ProjectService(setup_session).create(ProjectCreate(name="Original"))
        project_id = project.id

    with Session(engine) as first_session, Session(engine) as stale_session:
        first_service = ProjectService(first_session)
        stale_service = ProjectService(stale_session)
        assert first_service.get(project_id).version == 1
        stale_copy = stale_service.get(project_id)
        assert stale_copy.version == 1

        first_service.update(project_id, ProjectUpdate(description="First", version=1))
        with pytest.raises(DomainError, match="modified") as conflict:
            stale_service.update(project_id, ProjectUpdate(description="Stale", version=1))
        assert conflict.value.status == 409

    with Session(engine) as verification_session:
        current = ProjectService(verification_session).get(project_id)
        assert current.description == "First"
        assert current.version == 2
