from __future__ import annotations

from datetime import datetime as dt, timezone as tz

from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from db.models.base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    # Profile fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    linkedin_url: Mapped[str] = mapped_column(String(255), nullable=True)
    github_url: Mapped[str] = mapped_column(String(255), nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Authentication fields
    auth_provider: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # e.g., 'google', 'github'
    auth_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # Unique ID from the auth provider

    # Timestamps
    created_at: Mapped[dt] = mapped_column(default=dt.now(tz=tz.utc), nullable=False)
    updated_at: Mapped[dt] = mapped_column(
        default=dt.now(tz=tz.utc), onupdate=dt.now(tz=tz.utc), nullable=False
    )

    # Relationships
    applications: Mapped[list["Application"]] = relationship(
        "Application", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<UserProfile(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}')>"
