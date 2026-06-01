from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.group import Group
    from app.models.role import Role


class DocumentPageRole(Base):
    __tablename__ = "document_page_roles"

    page_id: Mapped[int] = mapped_column(ForeignKey("document_pages.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)


class DocumentPageGroup(Base):
    __tablename__ = "document_page_groups"

    page_id: Mapped[int] = mapped_column(ForeignKey("document_pages.id", ondelete="CASCADE"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True)


class DocumentPage(Base):
    __tablename__ = "document_pages"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_document_pages_slug"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(500), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(700), nullable=False)
    access_mode: Mapped[str] = mapped_column(String(20), server_default=text("'public'"), default="public", nullable=False)
    is_listed: Mapped[bool] = mapped_column(server_default=text("true"), default=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    roles: Mapped[list["Role"]] = relationship(
        secondary="document_page_roles",
        back_populates="pages",
        lazy="selectin",
    )
    groups: Mapped[list["Group"]] = relationship(
        secondary="document_page_groups",
        back_populates="pages",
        lazy="selectin",
    )
