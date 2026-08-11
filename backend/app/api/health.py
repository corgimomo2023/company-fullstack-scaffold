from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas import Health

router = APIRouter(prefix="/health", tags=["health"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/live", response_model=Health, response_model_exclude_none=True)
def live() -> Health:
    return Health(status="ok")


@router.get("/ready", response_model=Health)
def ready(session: SessionDep) -> Health:
    session.execute(text("SELECT 1"))
    return Health(status="ready", database="ok")
