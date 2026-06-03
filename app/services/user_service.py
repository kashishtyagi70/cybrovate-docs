from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import Role, User
from app.schemas.user import UserCreate, UserUpdate
from app.security import hash_password


class DuplicateUserError(ValueError):
    pass


def create_user(db: Session, user_in: UserCreate) -> User:
    user_data = user_in.model_dump()
    password = user_data.pop("password", None)
    user = User(**user_data)
    if password:
        user.password_hash = hash_password(password)
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateUserError("Username or email already exists") from exc
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_with_roles(db: Session, user_id: int) -> User | None:
    statement = select(User).options(selectinload(User.roles), selectinload(User.groups)).where(User.id == user_id)
    return db.scalar(statement)


def get_user_by_username(db: Session, username: str) -> User | None:
    statement = select(User).options(selectinload(User.roles), selectinload(User.groups)).where(User.username == username)
    return db.scalar(statement)


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).options(selectinload(User.roles), selectinload(User.groups)).where(User.email == email)
    return db.scalar(statement)


def get_user_by_username_or_email(db: Session, identifier: str) -> User | None:
    statement = (
        select(User)
        .options(selectinload(User.roles), selectinload(User.groups))
        .where((User.username == identifier) | (User.email == identifier))
    )
    return db.scalar(statement)


def has_password_enabled_user(db: Session) -> bool:
    statement = select(User.id).where(User.password_hash.is_not(None)).limit(1)
    return db.scalar(statement) is not None


def user_has_role(user: User, role_name: str) -> bool:
    return user.role == role_name or any(role.name == role_name for role in user.roles)


def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    statement = select(User).order_by(User.id).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    password = update_data.pop("password", None)
    for field, value in update_data.items():
        setattr(user, field, value)
    if password:
        user.password_hash = hash_password(password)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateUserError("Username or email already exists") from exc
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()


def reset_password(db: Session, user: User, password: str) -> User:
    user.password_hash = hash_password(password)
    db.commit()
    db.refresh(user)
    return user


def assign_role(db: Session, user: User, role: Role) -> User:
    if role not in user.roles:
        user.roles.append(role)
        db.commit()
        db.refresh(user)
    return user
