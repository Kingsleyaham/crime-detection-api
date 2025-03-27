from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import Session

from app.api.services.user_service import UserService
from app.core.database import get_session
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup(user_data:UserCreate, db:Session = Depends(get_session)):
    return await UserService.create_user(db, user_data)

@router.post("/login")
async def login():
    pass

@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user