from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.errors import DomainError
from app.models import Project
from app.repositories import ProjectRepository
from app.schemas import ProjectCreate, ProjectUpdate


class ProjectService:
    """Coordinates business rules and the transaction boundary for one use case."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = ProjectRepository(session)

    def list(self, *, limit: int, offset: int) -> tuple[list[Project], int]:
        return self.repository.list(limit=limit, offset=offset)

    def get(self, project_id: int) -> Project:
        project = self.repository.get(project_id)
        if project is None:
            raise DomainError(404, "Not found", "Project does not exist", "not-found")
        return project

    def create(self, data: ProjectCreate) -> Project:
        try:
            project = self.repository.add(data)
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise DomainError(409, "Conflict", "Project name already exists", "conflict") from exc
        self.session.refresh(project)
        return project

    def update(self, project_id: int, data: ProjectUpdate) -> Project:
        project = self.get(project_id)
        if project.version != data.version:
            raise DomainError(
                409, "Conflict", "Project was modified by another request", "conflict"
            )
        try:
            updated = self.repository.apply_update(project_id, data)
            if updated is None:
                self.session.rollback()
                raise DomainError(
                    409, "Conflict", "Project was modified by another request", "conflict"
                )
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise DomainError(409, "Conflict", "Project name already exists", "conflict") from exc
        except DomainError:
            raise
        except Exception:
            self.session.rollback()
            raise
        self.session.refresh(updated)
        return updated

    def delete(self, project_id: int) -> None:
        project = self.get(project_id)
        try:
            self.repository.remove(project)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
