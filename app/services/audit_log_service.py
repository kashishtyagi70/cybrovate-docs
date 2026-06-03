from sqlalchemy.orm import Session

from app.models import AuditLog


def log_action(db: Session, user_id: int | None, action: str, details: str | None = None) -> None:
    db.add(AuditLog(user_id=user_id, action=action, details=details))
    db.commit()
