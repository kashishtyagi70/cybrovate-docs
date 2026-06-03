from pathlib import Path

from sqlalchemy.orm import Session

from app.models import User
from app.schemas.document import DocumentCreate
from app.services import category_service, document_service
from app.utils.slug import slugify

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = BASE_DIR / "docs"


def _title_from_path(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").title()


def _category_from_path(path: Path) -> str:
    parts = path.relative_to(DOCS_DIR).parts
    if len(parts) > 1:
        return parts[-2].replace("_", " ").replace("-", " ").title()
    return "General"


def import_docs_from_files(db: Session, user: User | None = None, docs_dir: Path = DOCS_DIR) -> dict[str, int]:
    imported = 0
    updated = 0
    skipped = 0

    if not docs_dir.exists():
        return {"imported": 0, "updated": 0, "skipped": 0}

    for markdown_path in sorted(docs_dir.rglob("*.md")):
        relative_slug = markdown_path.relative_to(docs_dir).with_suffix("").as_posix()
        slug = slugify(relative_slug)
        title = _title_from_path(markdown_path)
        content = markdown_path.read_text(encoding="utf-8")
        category = category_service.get_or_create_category(db, _category_from_path(markdown_path))
        existing = document_service.get_document_by_slug(db, slug)

        if existing is None:
            document_service.create_document(
                db,
                DocumentCreate(
                    title=title,
                    slug=slug,
                    content=content,
                    category_id=category.id,
                    visibility="public",
                    is_published=True,
                ),
                user,
            )
            imported += 1
        elif existing.title != title or existing.content != content or existing.category_id != category.id:
            from app.schemas.document import DocumentUpdate

            document_service.update_document(
                db,
                existing,
                DocumentUpdate(title=title, content=content, category_id=category.id),
                user,
            )
            updated += 1
        else:
            skipped += 1

    return {"imported": imported, "updated": updated, "skipped": skipped}


def main() -> None:
    from app.database import SessionLocal

    with SessionLocal() as db:
        result = import_docs_from_files(db)
        print(
            f"Imported {result['imported']} documents; "
            f"updated {result['updated']}; skipped {result['skipped']} unchanged."
        )


if __name__ == "__main__":
    main()
