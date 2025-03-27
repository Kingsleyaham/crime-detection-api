import uuid

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies import CurrentUserDep
from app.api.services.shift_service import ShiftService
from app.api.services.auth_service import CurrentUserToken
from app.core.database import get_session
from app.schemas.shift import ShiftResponse, ShiftCreate, ShiftDeleteResponse, ShiftUpdate, ShiftUpdateResponse

router = APIRouter()


@router.get("/", response_model=ShiftResponse, status_code=200)
async def read_shifts(current_user: CurrentUserDep, token: CurrentUserToken, db: Session = Depends(get_session)):
    return await ShiftService.get_shifts(db, current_user.id)


@router.post("/", response_model=ShiftResponse, status_code=201)
async def create_shift(user_data: ShiftCreate, current_user: CurrentUserDep, token: CurrentUserToken,
                       db: Session = Depends(get_session)
                       ):
    return await ShiftService.create_shift(db, user_data, current_user.id)


@router.get("/{shift_id}", response_model=ShiftResponse, status_code=200)
async def read_shift(shift_id: uuid.UUID, current_user: CurrentUserDep, token: CurrentUserToken,
                     db: Session = Depends(get_session)):
    return await ShiftService.get_shift(db, current_user.id, shift_id)


@router.patch("/{shift_id}", response_model=ShiftUpdateResponse, status_code=200)
async def update_shift(user_data:ShiftUpdate, shift_id: uuid.UUID, current_user: CurrentUserDep, token: CurrentUserToken, db: Session = Depends(get_session)):
    return await ShiftService.update_shift(db, current_user.id, shift_id, user_data)


@router.delete("/{shift_id}", response_model=ShiftDeleteResponse, status_code=200)
async def delete_shift(shift_id: uuid.UUID, current_user: CurrentUserDep, token: CurrentUserToken,
                       db: Session = Depends(get_session)
                       ):
    return await ShiftService.delete_shift(db, current_user.id, shift_id)
