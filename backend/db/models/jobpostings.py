from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import func


from db.models.base import Base


class JobPosting(Base):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    company: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(nullable=True)

    # Dates
    date_posted: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
