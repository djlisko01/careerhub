from __future__ import annotations

import enum

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Enum as SQLAlchemyEnum

from db.models.base import BaseModel


class PrincipalType(enum.Enum):
    HUMAN = "HUMAN"
    AI_AGENT = "AI_AGENT"


class Principal(BaseModel):
    __tablename__ = "principals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    principal_type: Mapped[PrincipalType] = mapped_column(
        SQLAlchemyEnum(PrincipalType), nullable=False
    )
