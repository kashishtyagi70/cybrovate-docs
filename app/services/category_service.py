from sqlalchemy.orm import Session

from app.models import Category
from app.repositories import category_repository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.slug import slugify


class DuplicateCategoryError(ValueError):
    pass


def list_categories(db: Session) -> list[Category]:
    return category_repository.list_categories(db)


def get_category(db: Session, category_id: int) -> Category | None:
    return category_repository.get_by_id(db, category_id)


def get_or_create_category(db: Session, name: str) -> Category:
    existing = category_repository.get_by_name(db, name)
    if existing:
        return existing
    return create_category(db, CategoryCreate(name=name))


def create_category(db: Session, category_in: CategoryCreate) -> Category:
    slug = category_in.slug or slugify(category_in.name)
    if category_repository.get_by_slug(db, slug):
        raise DuplicateCategoryError("Category slug already exists")
    return category_repository.create(db, category_in.name, slug)


def update_category(db: Session, category: Category, category_in: CategoryUpdate) -> Category:
    name = category_in.name or category.name
    slug = category_in.slug or slugify(name)
    existing = category_repository.get_by_slug(db, slug)
    if existing and existing.id != category.id:
        raise DuplicateCategoryError("Category slug already exists")
    return category_repository.update(db, category, name, slug)


def delete_category(db: Session, category: Category) -> None:
    category_repository.delete(db, category)
