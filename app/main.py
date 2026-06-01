"""FastAPI application for the Cybrovate documentation platform."""

from pathlib import Path
from typing import Any

import markdown
from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.models import DocumentPage
from app.routers import audit_logs, roles, users
from app.schemas.group import GroupCreate
from app.schemas.user import UserCreate
from app.security import SESSION_COOKIE_NAME, SESSION_MAX_AGE_SECONDS, create_session_token, read_session_user_id, verify_password
from app.services import group_service, page_service, role_service, user_service


BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
IMAGES_DIR = BASE_DIR / "Images"

MARKDOWN_EXTENSIONS = ["fenced_code", "tables", "toc"]
MARKDOWN_EXTENSION_CONFIGS = {"toc": {"toc_depth": "1-3"}}
TITLE_ACRONYMS = {"api", "aws", "css", "gcp", "html", "http", "https", "iam", "ip", "sdk", "ui", "url"}

app = FastAPI(title="Cybrovate Docs", docs_url="/api-docs", redoc_url=None)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")

app.include_router(users.router)
app.include_router(roles.router)
app.include_router(audit_logs.router)


def get_optional_user(request: Request, db: Session) -> Any | None:
    user_id = read_session_user_id(request)
    if user_id is None:
        return None
    return user_service.get_user_with_roles(db, user_id)


def get_template_user(request: Request) -> Any | None:
    with SessionLocal() as db:
        return get_optional_user(request, db)


def require_admin_user(request: Request, db: Session = Depends(get_db)) -> Any:
    user = get_optional_user(request, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/login"})
    if not user.is_active or not user_service.user_has_role(user, "Admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


def format_title(slug: str) -> str:
    """Turn file/folder names like aws-onboarding into AWS Onboarding."""
    words = slug.replace("_", " ").replace("-", " ").split()
    return " ".join(
        word.upper() if word.lower() in TITLE_ACRONYMS else word[:1].upper() + word[1:].lower()
        for word in words
        if word
    )


def normalize_page_slug(page: str) -> str:
    """Normalize incoming URLs so Windows and browser paths behave the same."""
    normalized = page.replace("\\", "/").strip("/")
    if normalized.endswith(".md"):
        normalized = normalized[:-3]
    return normalized


def build_navigation(directory: Path = DOCS_DIR, allowed_slugs: set[str] | None = None) -> list[dict[str, Any]]:
    """Build the sidebar tree from folders and .md files inside docs/."""
    if not directory.exists():
        return []

    items: list[dict[str, Any]] = []
    children = sorted(
        directory.iterdir(),
        key=lambda item: (not item.is_dir(), format_title(item.stem if item.is_file() else item.name)),
    )

    for child in children:
        if child.is_dir():
            child_items = build_navigation(child, allowed_slugs)
            if child_items:
                items.append(
                    {
                        "type": "section",
                        "title": format_title(child.name),
                        "children": child_items,
                    }
                )
        elif child.is_file() and child.suffix.lower() == ".md":
            slug = child.relative_to(DOCS_DIR).with_suffix("").as_posix()
            if allowed_slugs is not None and slug not in allowed_slugs:
                continue
            items.append(
                {
                    "type": "page",
                    "title": format_title(child.stem),
                    "slug": slug,
                }
            )

    return items


def build_public_navigation(request: Request | None = None) -> list[dict[str, Any]]:
    with SessionLocal() as db:
        page_service.sync_pages_from_files(db, DOCS_DIR, format_title)
        user = get_optional_user(request, db) if request is not None else None
        allowed_slugs = page_service.get_accessible_listed_slugs(db, user)
    return build_navigation(allowed_slugs=allowed_slugs)


def find_first_page(items: list[dict[str, Any]]) -> str | None:
    """Return the first page slug in a navigation branch."""
    for item in items:
        if item["type"] == "page":
            return item["slug"]

        first_child = find_first_page(item["children"])
        if first_child:
            return first_child

    return None


def resolve_docs_path(slug: str) -> Path:
    """Resolve a URL slug under docs/ and reject paths outside docs/."""
    resolved_path = (DOCS_DIR / slug).resolve()
    docs_root = DOCS_DIR.resolve()

    try:
        resolved_path.relative_to(docs_root)
    except ValueError:
        raise HTTPException(status_code=404, detail="Page not found")

    return resolved_path


def find_first_page_in_directory(slug: str, allowed_slugs: set[str] | None = None) -> str | None:
    """Map folder URLs like /onboarding to the first markdown page inside."""
    directory = resolve_docs_path(slug)
    if not directory.is_dir():
        return None
    return find_first_page(build_navigation(directory, allowed_slugs))


def build_breadcrumbs(page: str) -> list[dict[str, str]]:
    """Create breadcrumb links from the current page path."""
    parts = normalize_page_slug(page).split("/")
    breadcrumbs: list[dict[str, str]] = [{"title": "Docs", "href": "/"}]

    for index, part in enumerate(parts):
        slug = "/".join(parts[: index + 1])
        breadcrumbs.append(
            {
                "title": format_title(part),
                "href": f"/{slug}",
            }
        )

    return breadcrumbs


def get_markdown_path(page: str) -> Path:
    """Convert a route slug into the expected markdown file path."""
    slug = normalize_page_slug(page)
    return resolve_docs_path(f"{slug}.md")


def flatten_toc(tokens: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flatten Python-Markdown's nested TOC tokens for simple template loops."""
    items: list[dict[str, Any]] = []

    for token in tokens:
        items.append(
            {
                "id": token["id"],
                "name": token["name"],
                "level": token["level"],
            }
        )
        items.extend(flatten_toc(token.get("children", [])))

    return items


def render_markdown(page: str) -> dict[str, Any] | None:
    """Read one markdown file and return rendered HTML plus heading links."""
    file_path = get_markdown_path(page)
    if not file_path.is_file():
        return None

    raw = file_path.read_text(encoding="utf-8")
    renderer = markdown.Markdown(
        extensions=MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWN_EXTENSION_CONFIGS,
        output_format="html5",
    )
    content = renderer.convert(raw)
    toc_items = flatten_toc(renderer.toc_tokens)
    toc_items = [item for item in toc_items if item["level"] > 1]

    return {"content": content, "toc_items": toc_items}


@app.get("/login")
def login_page(request: Request, db: Session = Depends(get_db)):
    if get_optional_user(request, db) is not None:
        return RedirectResponse(url="/admin/dashboard")

    return templates.TemplateResponse(
        request,
        "login.html",
        {
            "page_title": "Login",
            "setup_mode": not user_service.has_password_enabled_user(db),
            "error": None,
        },
    )


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = user_service.get_user_by_username(db, username)
    if user is None or not user.is_active or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "page_title": "Login",
                "setup_mode": not user_service.has_password_enabled_user(db),
                "error": "Invalid username or password.",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    response = RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        create_session_token(user.id),
        max_age=SESSION_MAX_AGE_SECONDS,
        httponly=True,
        samesite="lax",
    )
    return response


@app.post("/setup")
def setup_admin(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    if user_service.has_password_enabled_user(db):
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    admin_role = next((role for role in role_service.list_roles(db) if role.name == "Admin"), None)
    if admin_role is None:
        raise HTTPException(status_code=500, detail="Admin role is missing. Run database migrations.")

    try:
        user = user_service.create_user(
            db,
            UserCreate(
                username=username,
                email=email,
                full_name=full_name,
                password=password,
                is_active=True,
            ),
        )
    except user_service.DuplicateUserError as exc:
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "page_title": "Login",
                "setup_mode": True,
                "error": str(exc),
            },
            status_code=status.HTTP_409_CONFLICT,
        )

    user_service.assign_role(db, user, admin_role)
    response = RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        create_session_token(user.id),
        max_age=SESSION_MAX_AGE_SECONDS,
        httponly=True,
        samesite="lax",
    )
    return response


@app.post("/logout")
def logout() -> Response:
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response


@app.get("/admin/dashboard")
def admin_dashboard(request: Request, db: Session = Depends(get_db), current_user: Any = Depends(require_admin_user)):
    pages = page_service.sync_pages_from_files(db, DOCS_DIR, format_title)
    return templates.TemplateResponse(
        request,
        "admin_dashboard.html",
        {
            "page_title": "Admin Dashboard",
            "pages": pages,
            "roles": role_service.list_roles(db),
            "groups": group_service.list_groups(db),
            "current_user": current_user,
        },
    )


@app.post("/admin/groups")
def create_group(
    name: str = Form(...),
    description: str | None = Form(None),
    db: Session = Depends(get_db),
    current_user: Any = Depends(require_admin_user),
):
    try:
        group_service.create_group(db, GroupCreate(name=name, description=description))
    except group_service.DuplicateGroupError:
        pass
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/admin/pages/{page_id}/access")
def update_page_access(
    page_id: int,
    access_mode: str = Form(...),
    is_listed: bool = Form(False),
    role_ids: list[int] | None = Form(None),
    group_ids: list[int] | None = Form(None),
    notes: str | None = Form(None),
    db: Session = Depends(get_db),
    current_user: Any = Depends(require_admin_user),
):
    page = db.get(DocumentPage, page_id)
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")

    try:
        page_service.update_page_access(
            db,
            page,
            access_mode=access_mode,
            is_listed=is_listed,
            role_ids=role_ids or [],
            group_ids=group_ids or [],
            notes=notes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/")
async def home(request: Request):
    navigation = build_public_navigation(request)
    first_page = find_first_page(navigation)
    docs_entry_url = f"/{first_page}" if first_page else "#"

    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "navigation": navigation,
            "docs_entry_url": docs_entry_url,
            "page_title": "Home",
            "current_user": get_template_user(request),
        },
    )


@app.get("/docs")
async def docs_entry(request: Request):
    first_page = find_first_page(build_public_navigation(request))

    if first_page:
        return RedirectResponse(url=f"/{first_page}")

    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "navigation": [],
            "docs_entry_url": "#",
            "page_title": "Home",
            "current_user": get_template_user(request),
        },
    )


@app.get("/{page:path}")
async def docs(request: Request, page: str):
    current_page = normalize_page_slug(page)
    navigation = build_public_navigation(request)
    first_page = find_first_page(navigation)
    docs_entry_url = f"/{first_page}" if first_page else "#"

    with SessionLocal() as db:
        page_service.sync_pages_from_files(db, DOCS_DIR, format_title)
        user = get_optional_user(request, db)
        public_slugs = page_service.get_accessible_listed_slugs(db, user)

    first_nested_page = find_first_page_in_directory(current_page, public_slugs)
    if first_nested_page:
        return RedirectResponse(url=f"/{first_nested_page}")

    with SessionLocal() as db:
        page_service.sync_pages_from_files(db, DOCS_DIR, format_title)
        user = get_optional_user(request, db)
        page_meta = page_service.get_page_by_slug(db, current_page)
        if page_meta is not None and not page_service.can_user_access_page(page_meta, user):
            raise HTTPException(
                status_code=403,
                detail="This page is restricted.",
            )

    page_data = render_markdown(current_page)
    if page_data is None:
        raise HTTPException(status_code=404, detail="Page not found")

    return templates.TemplateResponse(
        request,
        "docs.html",
        {
            "content": page_data["content"],
            "toc_items": page_data["toc_items"],
            "navigation": navigation,
            "current_page": current_page,
            "breadcrumbs": build_breadcrumbs(current_page),
            "docs_entry_url": docs_entry_url,
            "page_title": format_title(current_page.rsplit("/", 1)[-1]),
            "current_user": get_template_user(request),
        },
    )
