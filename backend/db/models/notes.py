from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Text, String, func

from db.models.base import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Content
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text)

    # Dates
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    # relationships
    application: Mapped["Application"] = relationship(
        "Application", back_populates="notes"
    )
