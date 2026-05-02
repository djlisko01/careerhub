from __future__ import annotations

import enum
from datetime import datetime as dt, timezone as tz
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from db.models.base import Base


class ApplicationStatus(enum.Enum):
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    REJECTED = "rejected"


class PreferenceLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"), nullable=False)
    status: Mapped[ApplicationStatus] = mapped_column(default=ApplicationStatus.APPLIED, nullable=False)
    preference_level: Mapped[PreferenceLevel | None] = mapped_column(nullable=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job_postings.id"), nullable=False)

    # Dates
    applied_at: Mapped[dt] = mapped_column(nullable=False)
    updated_at: Mapped[dt] = mapped_column(default=dt.now(tz.utc), onupdate=dt.now(tz.utc), nullable=False)
    closed_at: Mapped[dt | None] = mapped_column(nullable=True)

    # Reltionship Objects
    user: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="applications"
    )
    job_posting: Mapped["JobPosting"] = relationship("JobPosting")
