import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field



class Notification(SQLModel, table=True):
    __tablename__ = "notifications"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    body: str
    is_read: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="users.id")

    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
