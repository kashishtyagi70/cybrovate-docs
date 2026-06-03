from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Category


def get_by_id(db: Session, category_id: int) -> Category | None:
    return db.get(Category, category_id)


def get_by_slug(db: Session, slug: str) -> Category | None:
    return db.scalar(select(Category).where(Category.slug == slug))


def get_by_name(db: Session, name: str) -> Category | None:
    return db.scalar(select(Category).where(func.lower(Category.name) == name.lower()))


def list_categories(db: Session) -> list[Category]:
    return list(db.scalars(select(Category).order_by(Category.name)).all())


def count_categories(db: Session) -> int:
    return db.scalar(select(func.count()).select_from(Category)) or 0


def create(db: Session, name: str, slug: str) -> Category:
    category = Category(name=name, slug=slug)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update(db: Session, category: Category, name: str, slug: str) -> Category:
    category.name = name
    category.slug = slug
    db.commit()
    db.refresh(category)
    return category


def delete(db: Session, category: Category) -> None:
    db.delete(category)
    db.commit()
