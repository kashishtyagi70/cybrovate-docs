from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.audit_log import AuditLogRead
from app.services import audit_service

router = APIRouter(prefix="/audit-logs", tags=["audit logs"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[AuditLogRead])
def list_audit_logs(db: DbSession, skip: int = 0, limit: int = 100) -> list[AuditLogRead]:
    return audit_service.list_audit_logs(db, skip=skip, limit=limit)
