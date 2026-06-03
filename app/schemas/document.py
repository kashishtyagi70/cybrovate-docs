from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.category import CategoryRead
from app.schemas.user import UserRead

DocumentVisibility = Literal["public", "private", "admin"]


class DocumentBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    slug: str | None = Field(default=None, max_length=500)
    content: str = ""
    category_id: int | None = None
    visibility: DocumentVisibility = "public"
    is_published: bool = False


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, max_length=500)
    content: str | None = None
    category_id: int | None = None
    visibility: DocumentVisibility | None = None
    is_published: bool | None = None


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    content: str
    category_id: int | None
    created_by: int | None
    visibility: DocumentVisibility
    is_published: bool
    created_at: datetime
    updated_at: datetime
    category: CategoryRead | None = None
    author: UserRead | None = None
