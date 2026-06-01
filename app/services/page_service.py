from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import DocumentPage, Group, Role, User

VALID_ACCESS_MODES = {"public", "roles", "groups"}


def discover_markdown_pages(docs_dir: Path, format_title: Any) -> list[dict[str, str]]:
    pages: list[dict[str, str]] = []
    if not docs_dir.exists():
        return pages

    for file_path in sorted(docs_dir.rglob("*.md")):
        slug = file_path.relative_to(docs_dir).with_suffix("").as_posix()
        pages.append(
            {
                "slug": slug,
                "title": format_title(file_path.stem),
                "file_path": file_path.relative_to(docs_dir.parent).as_posix(),
            }
        )

    return pages


def sync_pages_from_files(db: Session, docs_dir: Path, format_title: Any) -> list[DocumentPage]:
    discovered_pages = discover_markdown_pages(docs_dir, format_title)
    existing_by_slug = {
        page.slug: page
        for page in db.scalars(select(DocumentPage)).all()
    }

    for page_data in discovered_pages:
        page = existing_by_slug.get(page_data["slug"])
        if page is None:
            db.add(DocumentPage(**page_data))
        else:
            page.title = page_data["title"]
            page.file_path = page_data["file_path"]

    db.commit()
    return list_pages(db)


def list_pages(db: Session) -> list[DocumentPage]:
    statement = (
        select(DocumentPage)
        .options(selectinload(DocumentPage.roles), selectinload(DocumentPage.groups))
        .order_by(DocumentPage.slug)
    )
    return list(db.scalars(statement).all())


def get_page_by_slug(db: Session, slug: str) -> DocumentPage | None:
    statement = (
        select(DocumentPage)
        .options(selectinload(DocumentPage.roles), selectinload(DocumentPage.groups))
        .where(DocumentPage.slug == slug)
    )
    return db.scalar(statement)


def get_public_listed_slugs(db: Session) -> set[str]:
    statement = select(DocumentPage.slug).where(
        DocumentPage.access_mode == "public",
        DocumentPage.is_listed.is_(True),
    )
    return set(db.scalars(statement).all())


def get_accessible_listed_slugs(db: Session, user: User | None) -> set[str]:
    statement = (
        select(DocumentPage)
        .options(selectinload(DocumentPage.roles), selectinload(DocumentPage.groups))
        .where(DocumentPage.is_listed.is_(True))
    )
    return {page.slug for page in db.scalars(statement).all() if can_user_access_page(page, user)}


def can_user_access_page(page: DocumentPage, user: User | None) -> bool:
    if page.access_mode == "public":
        return True
    if user is None or not user.is_active:
        return False

    user_role_ids = {role.id for role in user.roles}
    user_group_ids = {group.id for group in user.groups}

    if page.access_mode == "roles":
        return bool(user_role_ids.intersection({role.id for role in page.roles}))
    if page.access_mode == "groups":
        return bool(user_group_ids.intersection({group.id for group in page.groups}))
    return False


def update_page_access(
    db: Session,
    page: DocumentPage,
    access_mode: str,
    is_listed: bool,
    role_ids: list[int],
    group_ids: list[int],
    notes: str | None = None,
) -> DocumentPage:
    if access_mode not in VALID_ACCESS_MODES:
        raise ValueError("Invalid access mode")

    roles = list(db.scalars(select(Role).where(Role.id.in_(role_ids))).all()) if role_ids else []
    groups = list(db.scalars(select(Group).where(Group.id.in_(group_ids))).all()) if group_ids else []

    page.access_mode = access_mode
    page.is_listed = is_listed
    page.notes = notes or None
    page.roles = roles if access_mode == "roles" else []
    page.groups = groups if access_mode == "groups" else []

    db.commit()
    db.refresh(page)
    return page
