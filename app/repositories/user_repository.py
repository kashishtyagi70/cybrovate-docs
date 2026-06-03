from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models import User


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_by_username(db: Session, username: str) -> User | None:
    statement = select(User).options(selectinload(User.roles), selectinload(User.groups)).where(User.username == username)
    return db.scalar(statement)


def list_users(db: Session, skip: int = 0, limit: int = 100, search: str | None = None) -> list[User]:
    statement = select(User).order_by(User.id).offset(skip).limit(limit)
    if search:
        pattern = f"%{search}%"
        statement = select(User).where(or_(User.username.ilike(pattern), User.email.ilike(pattern))).order_by(User.id).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def count_users(db: Session) -> int:
    return db.scalar(select(func.count()).select_from(User)) or 0


def has_password_enabled_user(db: Session) -> bool:
    return db.scalar(select(User.id).where(User.password_hash.is_not(None)).limit(1)) is not None


def create(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: User) -> User:
    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
