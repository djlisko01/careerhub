from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import SoftDeleteModel

if TYPE_CHECKING:
    from db.models.companies import Company
    from db.models.users import UserProfile


class UserAddress(SoftDeleteModel):
    __tablename__ = "user_addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), nullable=False)
    is_primary: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Relationships
    user: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="addresses"
    )
    address: Mapped["Address"] = relationship(
        "Address", back_populates="user_addresses"
    )


class CompanyAddress(SoftDeleteModel):
    __tablename__ = "company_addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), nullable=False)

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="addresses")
    address: Mapped["Address"] = relationship(
        "Address", back_populates="company_addresses"
    )


class Address(SoftDeleteModel):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)

    city: Mapped[str | None] = mapped_column(String(100))
    region: Mapped[str | None] = mapped_column(String(100))
    country_code: Mapped[str | None] = mapped_column(String(2))
    label: Mapped[str | None] = mapped_column(String(255))

    user_addresses: Mapped[list["UserAddress"]] = relationship(
        "UserAddress", back_populates="address"
    )
    company_addresses: Mapped[list["CompanyAddress"]] = relationship(
        "CompanyAddress", back_populates="address"
    )

    def __repr__(self):
        return f"<Address(id={self.id}, city='{self.city}', region='{self.region}', country_code='{self.country_code}')>"
