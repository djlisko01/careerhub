from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from db.models.base import TimestampedModel

if TYPE_CHECKING:
    from db.models.companies import Company


class JobPosting(TimestampedModel):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    location: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    post_url: Mapped[str] = mapped_column(nullable=True)

    # Dates
    date_posted: Mapped[datetime] = mapped_column(nullable=True)

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="job_postings")
