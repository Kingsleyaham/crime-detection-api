import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field


class Shift(SQLModel, table=True):
    __tablename__ = 'shifts'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str | None = Field(default=None)
    start_time: datetime
    end_time: datetime
    is_approved: bool = False
    user_id: uuid.UUID = Field(foreign_key="users.id")

    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())