from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Group
from app.schemas.group import GroupCreate


class DuplicateGroupError(ValueError):
    pass


def create_group(db: Session, group_in: GroupCreate) -> Group:
    group = Group(**group_in.model_dump())
    db.add(group)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateGroupError("Group name already exists") from exc
    db.refresh(group)
    return group


def get_group(db: Session, group_id: int) -> Group | None:
    return db.get(Group, group_id)


def list_groups(db: Session) -> list[Group]:
    statement = select(Group).order_by(Group.name)
    return list(db.scalars(statement).all())
