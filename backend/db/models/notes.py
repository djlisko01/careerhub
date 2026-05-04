from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, String

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

    # relationships
    application: Mapped["Application"] = relationship(
        "Application", back_populates="notes"
    )
