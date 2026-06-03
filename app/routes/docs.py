from typing import Annotated, Any

import markdown
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models import User
from app.services import document_service
from app.utils.markdown_media import expand_media_shortcodes

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db)]


def init(
    templates_obj: Jinja2Templates,
    markdown_extensions: list[str],
    markdown_extension_configs: dict[str, Any],
    flatten_toc_fn: Any,
    build_breadcrumbs_fn: Any,
) -> None:
    router.templates = templates_obj
    router.markdown_extensions = markdown_extensions
    router.markdown_extension_configs = markdown_extension_configs
    router.flatten_toc = flatten_toc_fn
    router.build_breadcrumbs = build_breadcrumbs_fn


@router.get("/docs")
def docs_index(request: Request, db: DbSession, current_user: User | None = Depends(get_current_user)):
    navigation = document_service.build_document_navigation(db, current_user)
    first_slug = None
    for section in navigation:
        children = section.get("children", [])
        if children:
            first_slug = children[0]["slug"]
            break

    if first_slug:
        return RedirectResponse(url=f"/docs/{first_slug}")

    return router.templates.TemplateResponse(
        request,
        "home.html",
        {
            "navigation": navigation,
            "docs_entry_url": "#",
            "page_title": "Home",
            "current_user": current_user,
        },
    )


@router.get("/docs/{slug:path}")
def render_document(request: Request, slug: str, db: DbSession, current_user: User | None = Depends(get_current_user)):
    document = document_service.get_document_by_slug(db, slug)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    if not document_service.can_user_access_document(document, current_user):
        raise HTTPException(status_code=403, detail="This document is restricted")

    renderer = markdown.Markdown(
        extensions=router.markdown_extensions,
        extension_configs=router.markdown_extension_configs,
        output_format="html5",
    )
    content = renderer.convert(expand_media_shortcodes(document.content))
    toc_items = router.flatten_toc(renderer.toc_tokens)
    toc_items = [item for item in toc_items if item["level"] > 1]
    navigation = document_service.build_document_navigation(db, current_user)

    return router.templates.TemplateResponse(
        request,
        "docs.html",
        {
            "content": content,
            "toc_items": toc_items,
            "navigation": navigation,
            "current_page": document.slug,
            "breadcrumbs": router.build_breadcrumbs(document.slug),
            "docs_entry_url": "/docs",
            "page_title": document.title,
            "current_user": current_user,
        },
    )
