import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator, ConfigDict

from app.constants.user_roles import UserRoleEnum
from app.schemas.response import ResponseModel


class BaseUser(BaseModel):
    email: EmailStr
    password: str

    # Define a validator for the password field
    @field_validator('password')
    def check_password(cls, value):
        # convert the password to a string if it is not already
        value = str(value)
        # check that the password has at least 8 characters, one uppercase letter, one lowercase letter, and one digit
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        if not any(c.isupper() for c in value):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not any(c.islower() for c in value):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not any(c.isdigit() for c in value):
            raise ValueError('Password must contain at least one digit.')
        return value


class UserCreate(BaseUser):
    firstname: str
    lastname: str
    phone: str | None = None
    role: UserRoleEnum = UserRoleEnum.USER


class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    phone: str | None = None
    role: UserRoleEnum | None = None


class UserLogin(BaseUser):
    pass


class BaseUserResponse(BaseModel):
    """
       Standard user response schema excluding sensitive information
       """
    id: uuid.UUID
    email: EmailStr
    firstname: str | None = None
    lastname: str | None = None
    phone: str | None = None
    is_active: bool = True
    role: UserRoleEnum

    created_at: datetime
    updated_at: datetime

    # This allows direct conversion from SQLModel User to this Pydantic model
    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    success: bool = True
    user: BaseUserResponse

class SignupResponse(UserResponse):
    """
    Response schema for successful signup
    """
    message: str | None = None

class LoginResponse(UserResponse):
    """Response schema for successful login"""
    access_token: str
    token_type: str