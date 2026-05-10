from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import TimestampedModel

if TYPE_CHECKING:
    from db.models.applications import Application
    from db.models.files import File


class Attachment(TimestampedModel):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id"), nullable=False)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id"), nullable=False
    )
    label: Mapped[str | None] = mapped_column(nullable=True)

    # relationships
    file: Mapped["File"] = relationship("File", back_populates="attachments")
    application: Mapped["Application"] = relationship(
        "Application", back_populates="attachments"
    )
