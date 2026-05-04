from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB

from db.models.base import Base


class File(Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id"), nullable=False
    )
    filename: Mapped[str] = mapped_column(nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False, unique=True)
    label: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    file_metadata: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    # relationships
    application: Mapped["Application"] = relationship(
        "Application", back_populates="attachments"
    )
