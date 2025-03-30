import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.constants.messages import MESSAGE


class NotificationCreate(BaseModel):
    title: str
    body: str
    user_id: uuid.UUID


class NotificationUpdate(BaseModel):
    is_read: bool


class NotificationBaseResponse(BaseModel):
    id: uuid.UUID
    title: str
    body: str
    is_read: bool

    created_at: datetime
    updated_at: datetime

    # This allows direct conversion from SQLModel User to this Pydantic model
    model_config = ConfigDict(from_attributes=True)


class NotificationResponse(BaseModel):
    success: bool = True
    data: NotificationBaseResponse
    message: str | None = None

class NotificationsResponse(BaseModel):
    success: bool = True
    data: list[NotificationBaseResponse]

class NotificationDeleteResponse(BaseModel):
    success: bool = True
    message: str = MESSAGE.DELETED


class NotificationCreateResponse(BaseModel):
    success: bool = True
    message: str = MESSAGE.CREATED
