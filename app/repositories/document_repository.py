from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models import Document


def get_by_id(db: Session, document_id: int) -> Document | None:
    return db.get(Document, document_id)


def get_by_slug(db: Session, slug: str) -> Document | None:
    statement = (
        select(Document)
        .options(selectinload(Document.category), selectinload(Document.author))
        .where(Document.slug == slug)
    )
    return db.scalar(statement)


def list_documents(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    published_only: bool = False,
) -> list[Document]:
    statement = select(Document).options(selectinload(Document.category), selectinload(Document.author))
    if published_only:
        statement = statement.where(Document.is_published.is_(True))
    if search:
        pattern = f"%{search}%"
        statement = statement.where(or_(Document.title.ilike(pattern), Document.slug.ilike(pattern), Document.content.ilike(pattern)))
    statement = statement.order_by(Document.updated_at.desc(), Document.id.desc()).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def count_documents(db: Session, published_only: bool = False, search: str | None = None) -> int:
    statement = select(func.count()).select_from(Document)
    if published_only:
        statement = statement.where(Document.is_published.is_(True))
    if search:
        pattern = f"%{search}%"
        statement = statement.where(or_(Document.title.ilike(pattern), Document.slug.ilike(pattern), Document.content.ilike(pattern)))
    return db.scalar(statement) or 0


def create(db: Session, document: Document) -> Document:
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def update(db: Session, document: Document) -> Document:
    db.commit()
    db.refresh(document)
    return document


def delete(db: Session, document: Document) -> None:
    db.delete(document)
    db.commit()
