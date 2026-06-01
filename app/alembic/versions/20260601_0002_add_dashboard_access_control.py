"""add dashboard access control

Revision ID: 20260601_0002
Revises: 20260601_0001
Create Date: 2026-06-01 16:10:00.000000
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260601_0002"
down_revision: str | None = "20260601_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "groups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_groups_id"), "groups", ["id"], unique=False)
    op.create_index(op.f("ix_groups_name"), "groups", ["name"], unique=True)

    op.create_table(
        "document_pages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(length=500), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("file_path", sa.String(length=700), nullable=False),
        sa.Column("access_mode", sa.String(length=20), server_default=sa.text("'public'"), nullable=False),
        sa.Column("is_listed", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug", name="uq_document_pages_slug"),
    )
    op.create_index(op.f("ix_document_pages_id"), "document_pages", ["id"], unique=False)

    op.create_table(
        "user_groups",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "group_id"),
    )

    op.create_table(
        "document_page_roles",
        sa.Column("page_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["page_id"], ["document_pages.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("page_id", "role_id"),
    )

    op.create_table(
        "document_page_groups",
        sa.Column("page_id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["page_id"], ["document_pages.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("page_id", "group_id"),
    )


def downgrade() -> None:
    op.drop_table("document_page_groups")
    op.drop_table("document_page_roles")
    op.drop_table("user_groups")
    op.drop_index(op.f("ix_document_pages_id"), table_name="document_pages")
    op.drop_table("document_pages")
    op.drop_index(op.f("ix_groups_name"), table_name="groups")
    op.drop_index(op.f("ix_groups_id"), table_name="groups")
    op.drop_table("groups")
