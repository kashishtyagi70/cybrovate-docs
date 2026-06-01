from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AuditLog


def list_audit_logs(db: Session, skip: int = 0, limit: int = 100) -> list[AuditLog]:
    statement = select(AuditLog).order_by(AuditLog.created_at.desc(), AuditLog.id.desc()).offset(skip).limit(limit)
    return list(db.scalars(statement).all())
