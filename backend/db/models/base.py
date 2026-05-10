from datetime import datetime

from sqlalchemy import func
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

CONVENTION = {
    "ix": "ix_%(column_0_label)s",  # indexes
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # unique constraints
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # check constraints
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # foreign keys
    "pk": "pk_%(table_name)s",  # primary keys
}


class BaseModel(DeclarativeBase):
    metadata = MetaData(naming_convention=CONVENTION)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)


class TimestampedModel(BaseModel, TimestampMixin):
    __abstract__ = True

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
