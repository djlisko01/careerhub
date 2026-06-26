from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from db.models.base import SoftDeleteModel

if TYPE_CHECKING:
    from db.models.companies import Company


class JobPosting(SoftDeleteModel):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    location: Mapped[str | None] = mapped_column()
    description: Mapped[str | None] = mapped_column()
    post_url: Mapped[str | None] = mapped_column()

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="job_postings")
