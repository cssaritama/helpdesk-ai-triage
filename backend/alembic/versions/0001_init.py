"""init

Revision ID: 0001
Revises: 
Create Date: 2026-01-13
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "kb_articles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body_markdown", sa.Text(), nullable=False),
        sa.Column("tags_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "tickets",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("requester_email", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "ticket_triage",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("ticket_id", sa.String(length=36), sa.ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("priority", sa.String(length=8), nullable=False),
        sa.Column("sentiment", sa.String(length=16), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("suggested_tags_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index("ix_ticket_triage_ticket_id", "ticket_triage", ["ticket_id"], unique=False)

    op.create_table(
        "ticket_reply_suggestions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("ticket_id", sa.String(length=36), sa.ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reply_markdown", sa.Text(), nullable=False),
        sa.Column("citations_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_ticket_reply_suggestions_ticket_id", "ticket_reply_suggestions", ["ticket_id"], unique=False)

def downgrade() -> None:
    op.drop_index("ix_ticket_reply_suggestions_ticket_id", table_name="ticket_reply_suggestions")
    op.drop_table("ticket_reply_suggestions")
    op.drop_index("ix_ticket_triage_ticket_id", table_name="ticket_triage")
    op.drop_table("ticket_triage")
    op.drop_table("tickets")
    op.drop_table("kb_articles")
