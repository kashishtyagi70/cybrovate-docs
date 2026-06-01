from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class GroupBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class GroupCreate(GroupBase):
    pass


class GroupRead(GroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
