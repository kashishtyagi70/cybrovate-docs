from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.group import GroupRead
from app.schemas.role import RoleRead

AccessMode = Literal["public", "roles", "groups"]


class DocumentPageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    file_path: str
    access_mode: AccessMode
    is_listed: bool
    notes: str | None
    created_at: datetime
    updated_at: datetime
    roles: list[RoleRead] = Field(default_factory=list)
    groups: list[GroupRead] = Field(default_factory=list)
