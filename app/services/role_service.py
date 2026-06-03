from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Role
from app.schemas.role import RoleCreate


class DuplicateRoleError(ValueError):
    pass


def create_role(db: Session, role_in: RoleCreate) -> Role:
    role = Role(**role_in.model_dump())
    db.add(role)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateRoleError("Role name already exists") from exc
    db.refresh(role)
    return role


def get_role(db: Session, role_id: int) -> Role | None:
    return db.get(Role, role_id)


def get_role_by_name(db: Session, name: str) -> Role | None:
    statement = select(Role).where(Role.name == name)
    return db.scalar(statement)


def list_roles(db: Session, skip: int = 0, limit: int = 100) -> list[Role]:
    statement = select(Role).order_by(Role.id).offset(skip).limit(limit)
    return list(db.scalars(statement).all())
