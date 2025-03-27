from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlmodel import Session, select

from app.core.config import settings
from app.models.user import User
from app.schemas.auth import TokenData
from app.utils.password import verify_password

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

oauth2_password_bearer = OAuth2PasswordBearer(tokenUrl="login")



def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else :
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def authenticate_user(db:Session, email:str, password:str):
    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


CurrentUserToken = Annotated[str, Depends(oauth2_password_bearer)]