from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class UUIDModel(SQLModel):
    uuid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )

class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
        nullable=False
    )

class SoftDeleteModel(SQLModel):
    is_deleted: bool = Field(
        default=False,
        nullable=False
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        nullable=True
    )

class BaseModel(UUIDModel, TimestampModel, SoftDeleteModel):
    pass