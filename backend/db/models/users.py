from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from db.models.base import Base
from db.models.principals import PrincipalType

if TYPE_CHECKING:
    from db.models.address import Address
    from db.models.applications import Application
    from db.models.principals import Principal


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    linkedin_url: Mapped[str] = mapped_column(String(255), nullable=True)
    github_url: Mapped[str] = mapped_column(String(255), nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
    current_address_id: Mapped[int | None] = mapped_column(
        ForeignKey("addresses.id", use_alter=True, name="fk_user_current_address"),
        nullable=True,
    )

    principal_id: Mapped[int] = mapped_column(
        ForeignKey("principals.id"), nullable=False, unique=True
    )

    auth_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    auth_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ORM relationships
    applications: Mapped[list["Application"]] = relationship(
        "Application", back_populates="user", cascade="all, delete-orphan"
    )
    addresses: Mapped[list["Address"]] = relationship(
        "Address", foreign_keys="[Address.user_id]", back_populates="user"
    )
    current_address: Mapped["Address | None"] = relationship(
        "Address", foreign_keys="[UserProfile.current_address_id]", uselist=False
    )
    principal: Mapped["Principal"] = relationship("Principal", uselist=False)

    @validates("principal")
    def validate_principal(self, key, principal):
        if principal.principal_type != PrincipalType.HUMAN:
            raise ValueError(
                f"UserProfile principal must be HUMAN, got {principal.principal_type}"
            )
        return principal

    def __repr__(self):
        return f"<UserProfile(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}')>"
