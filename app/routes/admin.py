from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin_user
from app.database import get_db
from app.models import User
from app.repositories import category_repository, user_repository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.document import DocumentCreate, DocumentRead, DocumentUpdate
from app.schemas.user import UserCreate, UserUpdate
from app.services import category_service, document_service, user_service
from app.utils.import_docs import import_docs_from_files
from app.utils.slug import slugify

router = APIRouter(prefix="/admin")
DbSession = Annotated[Session, Depends(get_db)]


def init(templates_obj: Jinja2Templates) -> None:
    router.templates = templates_obj


def parse_optional_int(value: str | int | None) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


@router.get("/dashboard")
def dashboard(
    request: Request,
    db: DbSession,
    current_user: User = Depends(require_admin_user),
    q: str | None = None,
):
    documents = document_service.list_documents(db, limit=100, search=q)
    categories = category_service.list_categories(db)
    users = user_service.list_users(db, limit=100)
    doc_stats = document_service.stats(db)
    stats = {
        **doc_stats,
        "total_users": user_repository.count_users(db),
        "total_categories": category_repository.count_categories(db),
    }
    return router.templates.TemplateResponse(
        request,
        "admin_dashboard.html",
        {
            "page_title": "Admin Dashboard",
            "documents": documents,
            "categories": categories,
            "users": users,
            "stats": stats,
            "q": q or "",
            "current_user": current_user,
        },
    )


@router.post("/docs")
def create_document(
    db: DbSession,
    current_user: User = Depends(require_admin_user),
    title: str = Form(...),
    slug: str | None = Form(None),
    content: str = Form(...),
    category_id: str | None = Form(None),
    visibility: str = Form("public"),
    is_published: bool = Form(False),
):
    try:
        document_service.create_document(
            db,
            DocumentCreate(
                title=title,
                slug=slug or None,
                content=content,
                category_id=parse_optional_int(category_id),
                visibility=visibility,
                is_published=is_published,
            ),
            current_user,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/docs", response_model=list[DocumentRead])
def list_admin_documents(
    db: DbSession,
    current_user: User = Depends(require_admin_user),
    skip: int = 0,
    limit: int = 50,
    q: str | None = None,
):
    return document_service.list_documents(db, skip=skip, limit=limit, search=q)


@router.post("/docs/upload")
async def upload_markdown_document(
    db: DbSession,
    current_user: User = Depends(require_admin_user),
    file: UploadFile = File(...),
    title: str | None = Form(None),
    slug: str | None = Form(None),
    category_id: str | None = Form(None),
    visibility: str = Form("public"),
    is_published: bool = Form(True),
):
    filename = file.filename or "document.md"
    if not filename.lower().endswith(".md"):
        raise HTTPException(status_code=400, detail="Only .md files can be uploaded")

    raw_content = await file.read()
    try:
        content = raw_content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="Markdown file must be UTF-8 encoded") from exc

    document_title = title.strip() if title and title.strip() else filename.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title()
    document_slug = slugify(slug or filename.rsplit(".", 1)[0])

    try:
        document_service.create_document(
            db,
            DocumentCreate(
                title=document_title,
                slug=document_slug,
                content=content,
                category_id=parse_optional_int(category_id),
                visibility=visibility,
                is_published=is_published,
            ),
            current_user,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.put("/docs/{document_id}")
@router.post("/docs/{document_id}")
def update_document(
    document_id: int,
    db: DbSession,
    current_user: User = Depends(require_admin_user),
    title: str = Form(...),
    slug: str | None = Form(None),
    content: str = Form(...),
    category_id: str | None = Form(None),
    visibility: str = Form("public"),
    is_published: bool = Form(False),
):
    document = document_service.get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    try:
        document_service.update_document(
            db,
            document,
            DocumentUpdate(
                title=title,
                slug=slug or None,
                content=content,
                category_id=parse_optional_int(category_id),
                visibility=visibility,
                is_published=is_published,
            ),
            current_user,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.delete("/docs/{document_id}")
@router.post("/docs/{document_id}/delete")
def delete_document(document_id: int, db: DbSession, current_user: User = Depends(require_admin_user)):
    document = document_service.get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    document_service.delete_document(db, document, current_user)
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/docs/{document_id}/publish")
def toggle_publish(document_id: int, db: DbSession, current_user: User = Depends(require_admin_user)):
    document = document_service.get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    document_service.update_document(
        db,
        document,
        DocumentUpdate(is_published=not document.is_published),
        current_user,
    )
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/categories")
def create_category(
    db: DbSession,
    current_user: User = Depends(require_admin_user),
    name: str = Form(...),
    slug: str | None = Form(None),
):
    try:
        category_service.create_category(db, CategoryCreate(name=name, slug=slug or None))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/categories/{category_id}")
def update_category(
    category_id: int,
    db: DbSession,
    current_user: User = Depends(require_admin_user),
    name: str = Form(...),
    slug: str | None = Form(None),
):
    category = category_service.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category_service.update_category(db, category, CategoryUpdate(name=name, slug=slug or None))
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/categories/{category_id}/delete")
def delete_category(category_id: int, db: DbSession, current_user: User = Depends(require_admin_user)):
    category = category_service.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category_service.delete_category(db, category)
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/users")
def list_users(db: DbSession, current_user: User = Depends(require_admin_user)):
    return user_service.list_users(db)


@router.post("/users")
def create_user(
    db: DbSession,
    current_user: User = Depends(require_admin_user),
    username: str = Form(...),
    email: str = Form(...),
    full_name: str | None = Form(None),
    password: str = Form(...),
    role: str = Form("User"),
    is_active: bool = Form(True),
):
    try:
        user_service.create_user(
            db,
            UserCreate(
                username=username,
                email=email,
                full_name=full_name,
                password=password,
                role=role,
                is_active=is_active,
            ),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.put("/users/{user_id}")
@router.post("/users/{user_id}")
def update_user(
    user_id: int,
    db: DbSession,
    current_user: User = Depends(require_admin_user),
    username: str = Form(...),
    email: str = Form(...),
    full_name: str | None = Form(None),
    password: str | None = Form(None),
    role: str = Form("User"),
    is_active: bool = Form(False),
):
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_service.update_user(
        db,
        user,
        UserUpdate(
            username=username,
            email=email,
            full_name=full_name,
            password=password or None,
            role=role,
            is_active=is_active,
        ),
    )
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.delete("/users/{user_id}")
@router.post("/users/{user_id}/delete")
def delete_user(user_id: int, db: DbSession, current_user: User = Depends(require_admin_user)):
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot delete your own account")
    user_service.delete_user(db, user)
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/import-docs")
def import_docs(db: DbSession, current_user: User = Depends(require_admin_user)):
    import_docs_from_files(db, current_user)
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
