from sqlalchemy.orm import Session

from app.models import Document, User
from app.repositories import category_repository, document_repository
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.services import audit_log_service
from app.utils.slug import slugify

VALID_VISIBILITIES = {"public", "private", "admin"}


class DuplicateDocumentError(ValueError):
    pass


class InvalidDocumentError(ValueError):
    pass


def list_documents(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    published_only: bool = False,
) -> list[Document]:
    return document_repository.list_documents(db, skip=skip, limit=limit, search=search, published_only=published_only)


def get_document(db: Session, document_id: int) -> Document | None:
    return document_repository.get_by_id(db, document_id)


def get_document_by_slug(db: Session, slug: str) -> Document | None:
    return document_repository.get_by_slug(db, slug)


def create_document(db: Session, document_in: DocumentCreate, user: User | None) -> Document:
    slug = document_in.slug or slugify(document_in.title)
    if document_repository.get_by_slug(db, slug):
        raise DuplicateDocumentError("Document slug already exists")
    if document_in.visibility not in VALID_VISIBILITIES:
        raise InvalidDocumentError("Invalid visibility")
    if document_in.category_id and category_repository.get_by_id(db, document_in.category_id) is None:
        raise InvalidDocumentError("Category not found")

    document = Document(
        title=document_in.title,
        slug=slug,
        content=document_in.content,
        category_id=document_in.category_id,
        created_by=user.id if user else None,
        visibility=document_in.visibility,
        is_published=document_in.is_published,
    )
    created = document_repository.create(db, document)
    audit_log_service.log_action(db, user.id if user else None, "document.created", f"{created.id}:{created.slug}")
    return created


def update_document(db: Session, document: Document, document_in: DocumentUpdate, user: User | None) -> Document:
    data = document_in.model_dump(exclude_unset=True)
    if "title" in data and data["title"] is not None:
        document.title = data["title"]
    if "slug" in data and data["slug"]:
        slug = slugify(data["slug"])
        existing = document_repository.get_by_slug(db, slug)
        if existing and existing.id != document.id:
            raise DuplicateDocumentError("Document slug already exists")
        document.slug = slug
    if "content" in data and data["content"] is not None:
        document.content = data["content"]
    if "category_id" in data:
        category_id = data["category_id"]
        if category_id and category_repository.get_by_id(db, category_id) is None:
            raise InvalidDocumentError("Category not found")
        document.category_id = category_id
    if "visibility" in data and data["visibility"] is not None:
        if data["visibility"] not in VALID_VISIBILITIES:
            raise InvalidDocumentError("Invalid visibility")
        document.visibility = data["visibility"]
    if "is_published" in data and data["is_published"] is not None:
        document.is_published = data["is_published"]

    updated = document_repository.update(db, document)
    audit_log_service.log_action(db, user.id if user else None, "document.updated", f"{updated.id}:{updated.slug}")
    return updated


def delete_document(db: Session, document: Document, user: User | None) -> None:
    details = f"{document.id}:{document.slug}"
    document_repository.delete(db, document)
    audit_log_service.log_action(db, user.id if user else None, "document.deleted", details)


def can_user_access_document(document: Document, user: User | None) -> bool:
    if not document.is_published and (user is None or user.role != "Admin"):
        return False
    if document.visibility == "public":
        return True
    if document.visibility == "private":
        return user is not None and user.is_active
    if document.visibility == "admin":
        return user is not None and user.is_active and user.role == "Admin"
    return False


def build_document_navigation(db: Session, user: User | None) -> list[dict[str, object]]:
    documents = list_documents(db, limit=500, published_only=False)
    sections: dict[str, dict[str, object]] = {}

    for document in documents:
        if not can_user_access_document(document, user):
            continue
        category_name = document.category.name if document.category else "Uncategorized"
        section = sections.setdefault(
            category_name,
            {"type": "section", "title": category_name, "children": []},
        )
        section["children"].append(
            {
                "type": "page",
                "title": document.title,
                "slug": document.slug,
                "href": f"/docs/{document.slug}",
            }
        )

    return list(sections.values())


def stats(db: Session) -> dict[str, int]:
    return {
        "total_documents": document_repository.count_documents(db),
        "published_documents": document_repository.count_documents(db, published_only=True),
    }
