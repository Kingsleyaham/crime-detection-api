from typing import Annotated

from fastapi import HTTPException, Depends
from jwt import InvalidTokenError
from sqlmodel import Session, select

import jwt
from app.api.services.auth_service import  ALGORITHM
from app.constants.messages import MESSAGE
from app.core.config import settings
from app.core.database import get_session
from app.schemas.auth import TokenData
from app.models.user import User
from fastapi import Request

from app.schemas.user import UserResponse
from app.utils.helpers import extract_bearer_token


def get_token(request: Request):
    header = request.headers.get("Authorization")
    if header:
        token = extract_bearer_token(header)
        return token
    return ""

async def get_current_user(token: Annotated[str, Depends(get_token)], db: Session = Depends(get_session)):
    credential_exception = HTTPException(status_code=401, detail=MESSAGE.INVALID_TOKEN,
                                         headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credential_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credential_exception
    user = db.exec(select(User).where(User.email == token_data.email)).first()
    if not user:
        raise credential_exception

    return UserResponse(user=user)
