from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import BaseModel

if TYPE_CHECKING:
    from db.models.address import Address


class Company(BaseModel):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    current_address_id: Mapped[int | None] = mapped_column(
        ForeignKey("addresses.id", use_alter=True, name="fk_company_current_address"),
        nullable=True,
    )

    # Relationships
    addresses: Mapped[list["Address"]] = relationship(
        "Address", foreign_keys="[Address.company_id]", back_populates="company"
    )
    current_address: Mapped["Address | None"] = relationship(
        "Address", foreign_keys="[Company.current_address_id]", uselist=False
    )

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"
