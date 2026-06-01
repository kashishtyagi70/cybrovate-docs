"""FastAPI application for the Cybrovate documentation platform.

This project is filesystem-based: markdown files inside docs/ become web pages,
and folder structure becomes the sidebar navigation.
"""

import markdown
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
IMAGES_DIR = BASE_DIR / "Images"

# Markdown is the only content source for this MVP. The toc extension adds
# stable IDs to headings so the right-side "on this page" rail can link to them.
MARKDOWN_EXTENSIONS = ["fenced_code", "tables", "toc"]
MARKDOWN_EXTENSION_CONFIGS = {"toc": {"toc_depth": "1-3"}}
TITLE_ACRONYMS = {"api", "aws", "css", "gcp", "html", "http", "https", "iam", "ip", "sdk", "ui", "url"}

# Move FastAPI's built-in Swagger UI from /docs to /api-docs so /docs can be
# used as the user-facing documentation entry route.
app = FastAPI(title="Cybrovate Docs", docs_url="/api-docs", redoc_url=None)

# Jinja2 reads HTML templates from templates/.
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Static CSS is available at /static/style.css.
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Brand assets live in Images/. The topbar and browser tab use favicon.ico
# from this folder, so replacing Images/favicon.ico changes the visible logo.
app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")


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

    # Allow /getting-started/introduction.md and /getting-started/introduction
    # to point to the same markdown page.
    if normalized.endswith(".md"):
        normalized = normalized[:-3]
    return normalized


def build_navigation(directory: Path = DOCS_DIR) -> list[dict[str, Any]]:
    """Build the sidebar tree from folders and .md files inside docs/."""
    if not directory.exists():
        return []

    items: list[dict[str, Any]] = []

    # Sort folders before files, then sort everything alphabetically by title.
    children = sorted(
        directory.iterdir(),
        key=lambda item: (not item.is_dir(), format_title(item.stem if item.is_file() else item.name)),
    )

    for child in children:
        if child.is_dir():
            # A folder becomes a sidebar section only if it contains pages.
            child_items = build_navigation(child)
            if child_items:
                items.append(
                    {
                        "type": "section",
                        "title": format_title(child.name),
                        "children": child_items,
                    }
                )
        elif child.is_file() and child.suffix.lower() == ".md":
            # A markdown file becomes a clickable page link.
            slug = child.relative_to(DOCS_DIR).with_suffix("").as_posix()
            items.append(
                {
                    "type": "page",
                    "title": format_title(child.stem),
                    "slug": slug,
                }
            )

    return items


def find_first_page(items: list[dict[str, Any]]) -> str | None:
    """Return the first page slug in a navigation branch."""
    for item in items:
        # If this item is already a page, it is the first reachable page.
        if item["type"] == "page":
            return item["slug"]

        # Otherwise, search inside the folder/section.
        first_child = find_first_page(item["children"])
        if first_child:
            return first_child

    return None


def resolve_docs_path(slug: str) -> Path:
    """Resolve a URL slug under docs/ and reject paths outside docs/."""
    resolved_path = (DOCS_DIR / slug).resolve()
    docs_root = DOCS_DIR.resolve()

    # Security check: prevents URLs such as /../../secret.txt from escaping
    # the docs/ folder.
    try:
        resolved_path.relative_to(docs_root)
    except ValueError:
        raise HTTPException(status_code=404, detail="Page not found")

    return resolved_path


def find_first_page_in_directory(slug: str) -> str | None:
    """Map folder URLs like /onboarding to the first markdown page inside."""
    directory = resolve_docs_path(slug)

    # If the slug is not a folder, let the normal markdown renderer handle it.
    if not directory.is_dir():
        return None

    return find_first_page(build_navigation(directory))


def build_breadcrumbs(page: str) -> list[dict[str, str]]:
    """Create breadcrumb links from the current page path."""
    parts = normalize_page_slug(page).split("/")
    breadcrumbs: list[dict[str, str]] = [{"title": "Docs", "href": "/"}]

    # Build clickable crumbs for every path segment:
    # onboarding/cloud/aws-onboarding becomes Docs > Onboarding > Cloud > AWS Onboarding.
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
        # Each token is one heading from the markdown file.
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

    # Returning None lets the route decide whether to show a 404.
    if not file_path.is_file():
        return None

    raw = file_path.read_text(encoding="utf-8")

    # Python-Markdown converts markdown text into HTML. The same renderer also
    # exposes toc_tokens, which we use for the right-side heading list.
    renderer = markdown.Markdown(
        extensions=MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWN_EXTENSION_CONFIGS,
        output_format="html5",
    )
    content = renderer.convert(raw)
    toc_items = flatten_toc(renderer.toc_tokens)

    # The right-side rail should show section headings, not the page title.
    toc_items = [item for item in toc_items if item["level"] > 1]

    return {"content": content, "toc_items": toc_items}


@app.get("/")
async def home(request: Request):
    # The homepage is a landing page. Use /docs to enter the documentation.
    navigation = build_navigation()
    first_page = find_first_page(navigation)

    # If docs/ is empty, the button safely points nowhere instead of breaking.
    docs_entry_url = f"/{first_page}" if first_page else "#"

    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "navigation": navigation,
            "docs_entry_url": docs_entry_url,
            "page_title": "Home",
        },
    )


@app.get("/docs")
async def docs_entry(request: Request):
    # /docs always opens the first markdown page detected in docs/.
    first_page = find_first_page(build_navigation())

    # Redirect instead of rendering here so the browser URL becomes the real page.
    if first_page:
        return RedirectResponse(url=f"/{first_page}")

    # Empty-docs fallback. This rarely appears once markdown files exist.
    return templates.TemplateResponse(
        request,
        "home.html",
        {"navigation": [], "docs_entry_url": "#", "page_title": "Home"},
    )


@app.get("/{page:path}")
async def docs(request: Request, page: str):
    # This dynamic route catches any documentation page path, such as:
    # /getting-started/introduction or /onboarding/cloud/aws-onboarding.
    current_page = normalize_page_slug(page)
    navigation = build_navigation()
    first_page = find_first_page(navigation)
    docs_entry_url = f"/{first_page}" if first_page else "#"

    # Breadcrumbs can point to folders such as /onboarding. Redirect those
    # folder URLs to their first child page instead of returning a 404.
    first_nested_page = find_first_page_in_directory(current_page)
    if first_nested_page:
        return RedirectResponse(url=f"/{first_nested_page}")

    page_data = render_markdown(current_page)

    # If no matching .md file exists, FastAPI returns a clean 404 JSON response.
    if page_data is None:
        raise HTTPException(status_code=404, detail="Page not found")

    # Pass all page data into the docs template: rendered content, sidebar,
    # breadcrumbs, active page slug, and right-side heading links.
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
        },
    )
