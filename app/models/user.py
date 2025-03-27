import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field

from app.constants.user_roles import UserRoleEnum


class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    password: str
    firstname: str = Field(default=None)
    lastname: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    is_active: bool = Field(default=True)
    role: UserRoleEnum = Field(default=UserRoleEnum.USER.value)

    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
