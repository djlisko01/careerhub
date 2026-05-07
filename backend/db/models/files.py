from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.attachments import Attachment
    from db.models.principals import Principal


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("principals.id"), nullable=False)

    filename: Mapped[str] = mapped_column(nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False, unique=True)
    file_metadata: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    # relationships
    attachments: Mapped[list["Attachment"]] = relationship(
        "Attachment", back_populates="file", cascade="all, delete-orphan"
    )
    creator: Mapped["Principal"] = relationship("Principal")
