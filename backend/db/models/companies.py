from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import BaseModel

if TYPE_CHECKING:
    from db.models.address import Address, CompanyAddress
    from db.models.jobpostings import JobPosting


class Company(BaseModel):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    current_address_id: Mapped[int | None] = mapped_column(
        ForeignKey("addresses.id", use_alter=True, name="fk_company_current_address"),
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    job_postings: Mapped[list["JobPosting"]] = relationship(
        "JobPosting", back_populates="company"
    )
    addresses: Mapped[list["CompanyAddress"]] = relationship(
        "CompanyAddress", back_populates="company", cascade="all, delete-orphan"
    )
    current_address: Mapped["Address | None"] = relationship(
        "Address", foreign_keys=[current_address_id], uselist=False
    )

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"
