from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, func
from db.models.base import Base

if TYPE_CHECKING:
    from db.models.address import Address
    from db.models.users import UserProfile
    from backend.db.models.jobpostings import JobPosting


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
    status: Mapped[ApplicationStatus] = mapped_column(
        default=ApplicationStatus.APPLIED, nullable=False
    )
    preference_level: Mapped[PreferenceLevel | None] = mapped_column(nullable=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job_postings.id"), nullable=False)

    # Current Location
    current_location_id: Mapped[int | None] = mapped_column(
        ForeignKey("addresses.id"), nullable=True
    )

    # Dates
    applied_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )
    closed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    # Relationships
    user: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="applications"
    )
    job_posting: Mapped["JobPosting"] = relationship("JobPosting")
    current_location: Mapped["Address | None"] = relationship("Address", uselist=False)


class Reminders(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id"), nullable=False
    )
    reminder_date: Mapped[datetime] = mapped_column(nullable=False)
    message: Mapped[str | None] = mapped_column(nullable=True)
    is_completed: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    # Relationships
    application: Mapped["Application"] = relationship(
        "Application", back_populates="reminders"
    )
