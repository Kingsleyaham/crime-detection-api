from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlmodel import Session, select

from app.constants.messages import MESSAGE
from app.core.config import settings
from app.core.exceptions import IncorrectCredentialsException
from app.models.user import User
from app.schemas.auth import TokenData
from app.schemas.user import UserLogin, LoginResponse
from app.utils.password import verify_password

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 6 # 6 hours

oauth2_password_bearer = OAuth2PasswordBearer(tokenUrl="login")


class AuthService:
    @staticmethod
    def create_access_token(data:dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else :
            expire = datetime.now(timezone.utc) + timedelta(minutes=60)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    @staticmethod
    async def authenticate_user(db:Session, email:str, password:str) -> User | bool:
        user = db.exec(select(User).where(User.email == email)).first()
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user

    @staticmethod
    async def login(db:Session, form_data: UserLogin) -> LoginResponse:
        email, password = form_data.email, form_data.password
        user = await AuthService.authenticate_user(db, str(email), password)

        if not user:
            raise IncorrectCredentialsException(MESSAGE.INVALID_CREDENTIALS)

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires )

        return LoginResponse(user=user, access_token=access_token, token_type="bearer")


CurrentUserToken = Annotated[str, Depends(oauth2_password_bearer)]