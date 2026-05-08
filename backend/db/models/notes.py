from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, String

from db.models.base import TimestampedModel

if TYPE_CHECKING:
    from db.models.applications import Application


class Note(TimestampedModel):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Content
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text)

    # relationships
    application: Mapped["Application"] = relationship(
        "Application", back_populates="notes"
    )
