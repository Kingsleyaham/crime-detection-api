from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import Session

from app.api.services.auth_service import AuthService
from app.api.services.user_service import UserService
from app.core.database import get_session
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.user import UserCreate, LoginResponse, UserLogin, SignupResponse, UserResponse
from app.api.services.auth_service import CurrentUserToken
from app.api.dependencies import CurrentUserDep

router = APIRouter()


@router.post("/signup", response_model=SignupResponse, status_code=201)
async def signup(user_data: UserCreate, db: Session = Depends(get_session)):
    return await UserService.create_user(db, user_data)


@router.post("/login", response_model=LoginResponse, status_code=200)
async def login(user_data: UserLogin, db: Session = Depends(get_session)):
    return await AuthService.login(db, user_data)


@router.get("/users/me", response_model=UserResponse, status_code=200,)
async def read_users_me(current_user: CurrentUserDep, token: CurrentUserToken):
    return current_user
