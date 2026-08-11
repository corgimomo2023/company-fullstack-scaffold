from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.models import Project, utc_now
from app.schemas import ProjectCreate, ProjectUpdate


class ProjectRepository:
    """Persistence operations only; the service owns commit and rollback."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self, *, limit: int, offset: int) -> tuple[list[Project], int]:
        items = list(
            self.session.scalars(select(Project).order_by(Project.id).limit(limit).offset(offset))
        )
        total = self.session.scalar(select(func.count()).select_from(Project)) or 0
        return items, total

    def get(self, project_id: int) -> Project | None:
        return self.session.get(Project, project_id)

    def add(self, data: ProjectCreate) -> Project:
        project = Project(name=data.name, description=data.description)
        self.session.add(project)
        self.session.flush()
        return project

    def apply_update(self, project_id: int, data: ProjectUpdate) -> Project | None:
        changes = data.model_dump(exclude_unset=True, exclude={"version"})
        statement = (
            update(Project)
            .where(Project.id == project_id, Project.version == data.version)
            .values(**changes, version=data.version + 1, updated_at=utc_now())
            .returning(Project)
            .execution_options(populate_existing=True)
        )
        return self.session.scalars(statement).one_or_none()

    def remove(self, project: Project) -> None:
        self.session.delete(project)
        self.session.flush()
