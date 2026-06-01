from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.role import RoleRead


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    email: EmailStr
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool = True


class UserCreate(UserBase):
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class UserWithRoles(UserRead):
    roles: list[RoleRead] = Field(default_factory=list)
