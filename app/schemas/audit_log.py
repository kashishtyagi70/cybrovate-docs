from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuditLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
    action: str = Field(max_length=100)
    details: str | None
    created_at: datetime
