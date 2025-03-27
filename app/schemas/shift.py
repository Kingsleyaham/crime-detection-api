import uuid
from datetime import datetime

from pydantic import BaseModel, field_validator, ConfigDict

from app.constants.messages import MESSAGE


class BaseShift(BaseModel):
    name: str | None = None
    start_time: datetime
    end_time: datetime

    @field_validator('end_time')
    def validate_end_time(cls, end_time, info):
        start_time = info.data.get('start_time')
        if start_time is not None and end_time <= start_time:
            raise ValueError('End time must be later than start time.')
        return end_time


class ShiftCreate(BaseShift):
    id: uuid.UUID | None = None


class ShiftUpdate(BaseShift):
    start_time: datetime | None = None
    end_time: datetime | None = None
    is_approved: bool | None = None

    @field_validator('end_time')
    def validate_end_time(cls, end_time, info):
        start_time = info.data.get('start_time')
        if start_time is not None and end_time is not None and end_time <= start_time:
            raise ValueError('End time must be later than start time.')
        return end_time


class ShiftBaseResponse(BaseModel):
    id: uuid.UUID
    name: str | None = None
    start_time: datetime
    end_time: datetime
    is_approved: bool = False

    created_at: datetime
    updated_at: datetime

    # This allows direct conversion from SQLModel User to this Pydantic model
    model_config = ConfigDict(from_attributes=True)


class ShiftResponse(BaseModel):
    success: bool = True
    data: ShiftBaseResponse | list[ShiftBaseResponse]
    message: str | None = None


class ShiftDeleteResponse(BaseModel):
    success: bool = True
    message: str = MESSAGE.DELETED


class ShiftUpdateResponse(BaseModel):
    success: bool = True
    data: ShiftBaseResponse
    message: str = MESSAGE.UPDATED
