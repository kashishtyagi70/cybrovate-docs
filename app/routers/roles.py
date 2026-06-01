from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.role import RoleCreate, RoleRead
from app.services import role_service

router = APIRouter(prefix="/roles", tags=["roles"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(role_in: RoleCreate, db: DbSession) -> RoleRead:
    try:
        return role_service.create_role(db, role_in)
    except role_service.DuplicateRoleError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("", response_model=list[RoleRead])
def list_roles(db: DbSession, skip: int = 0, limit: int = 100) -> list[RoleRead]:
    return role_service.list_roles(db, skip=skip, limit=limit)
