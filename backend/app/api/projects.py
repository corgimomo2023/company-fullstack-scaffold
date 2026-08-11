from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas import ProjectCreate, ProjectList, ProjectRead, ProjectUpdate
from app.services import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("", response_model=ProjectList)
def list_projects(
    session: SessionDep, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0)
) -> ProjectList:
    items, total = ProjectService(session).list(limit=limit, offset=offset)
    return ProjectList(
        items=[ProjectRead.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, session: SessionDep) -> ProjectRead:
    return ProjectRead.model_validate(ProjectService(session).create(payload))


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, session: SessionDep) -> ProjectRead:
    return ProjectRead.model_validate(ProjectService(session).get(project_id))


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, payload: ProjectUpdate, session: SessionDep) -> ProjectRead:
    return ProjectRead.model_validate(ProjectService(session).update(project_id, payload))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, session: SessionDep) -> Response:
    ProjectService(session).delete(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
