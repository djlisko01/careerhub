from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from db.models.base import BaseModel
from db.models.principals import PrincipalType

if TYPE_CHECKING:
    from db.models.address import Address, UserAddress
    from db.models.applications import Application
    from db.models.principals import Principal


class UserProfile(BaseModel):
    __tablename__ = "user_profiles"
    __table_args__ = (
        UniqueConstraint("auth_provider", "auth_id", name="uq_user_auth"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    # Local login credentials
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # Authentication via external providers (e.g., OAuth)
    auth_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    auth_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # URLs for social profiles
    linkedin_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    github_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    current_address_id: Mapped[int | None] = mapped_column(
        ForeignKey("addresses.id", use_alter=True, name="fk_user_current_address"),
        nullable=True,
    )

    principal_id: Mapped[int] = mapped_column(
        ForeignKey("principals.id"), nullable=False, unique=True
    )


    # ORM relationships
    applications: Mapped[list["Application"]] = relationship(
        "Application", back_populates="user", cascade="all, delete-orphan"
    )
    addresses: Mapped[list["UserAddress"]] = relationship(
        "UserAddress", back_populates="user", cascade="all, delete-orphan"
    )
    current_address: Mapped["Address | None"] = relationship(
        "Address", foreign_keys=[current_address_id], uselist=False
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
