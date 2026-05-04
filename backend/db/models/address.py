from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.users import UserProfile
    from db.models.companies import Company


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int | None] = mapped_column(ForeignKey("user_profiles.id"), nullable=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), nullable=True)

    city: Mapped[str | None] = mapped_column(String(100))
    region: Mapped[str | None] = mapped_column(String(100))
    country_code: Mapped[str | None] = mapped_column(String(2))
    label: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    user: Mapped["UserProfile | None"] = relationship(
        "UserProfile", foreign_keys=[user_id], back_populates="addresses"
    )
    company: Mapped["Company | None"] = relationship(
        "Company", foreign_keys=[company_id], back_populates="addresses"
    )

    def __repr__(self):
        return f"<Address(id={self.id}, city='{self.city}', region='{self.region}', country_code='{self.country_code}')>"
