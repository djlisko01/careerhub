from datetime import datetime as dt, timezone as tz
from sqlalchemy.orm import mapped_column, Mapped

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
    date_posted: Mapped[dt] = mapped_column(nullable=True)
    created_at: Mapped[dt] = mapped_column(default=dt.now(tz.utc), nullable=False)
