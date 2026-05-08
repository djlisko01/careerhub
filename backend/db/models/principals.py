from __future__ import annotations

import enum

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import TimestampedModel


class PrincipalType(enum.Enum):
    HUMAN = "HUMAN"
    AI_AGENT = "AI_AGENT"


class Principal(TimestampedModel):
    __tablename__ = "principals"

    id: Mapped[int] = mapped_column(primary_key=True)
    principal_type: Mapped[PrincipalType] = mapped_column(
        SQLAlchemyEnum(PrincipalType), nullable=False
    )
