import http
import uuid
from datetime import datetime
from http import HTTPStatus

from dns.resolver import query
from sqlmodel import Session, select

from app.constants.messages import MESSAGE
from app.core.exceptions import AppException, NotFoundException
from app.models.shift import Shift
from app.schemas.shift import ShiftCreate, ShiftResponse, ShiftDeleteResponse, ShiftUpdate


class ShiftService:
    @staticmethod
    async def create_shift(db: Session, user_data: ShiftCreate, user_id: uuid.UUID):
        start_time, end_time = user_data.start_time, user_data.end_time
        existing_shift = db.exec(
            select(Shift).where((Shift.start_time == start_time) & (Shift.end_time == end_time)).where(
                Shift.id == user_id)).first()

        if existing_shift:
            raise AppException(
                message=MESSAGE.SHIFT_ALREADY_EXISTS,
                status_code=HTTPStatus.CONFLICT
            )

        shift = Shift(name=user_data.name, start_time=start_time, end_time=end_time, user_id=user_id)

        # save to database
        db.add(shift)
        db.commit()
        db.refresh(shift)

        return ShiftResponse(success=True, data=shift, message=MESSAGE.CREATED)

    @staticmethod
    async def get_shifts(db: Session, user_id: uuid.UUID):
        query = select(Shift).where(Shift.user_id == user_id)
        results = db.exec(query).all()

        return ShiftResponse(success=True, data=results)

    @staticmethod
    async def get_shift(db: Session, user_id: uuid.UUID, shift_id: uuid.UUID):
        query = select(Shift).where((Shift.user_id == user_id) & (Shift.id == shift_id))
        result = db.exec(query).first()

        return ShiftResponse(success=True, data=result)

    @staticmethod
    async def update_shift(db: Session, user_id: uuid.UUID, shift_id: uuid.UUID, update_data: ShiftUpdate = None):
        existing_shift = db.exec(select(Shift).where((Shift.user_id == user_id) & (Shift.id == shift_id))).first()
        if not existing_shift:
            raise NotFoundException(MESSAGE.SHIFT_NOT_FOUND)

        #     Prevent updating approved shifts
        if existing_shift.is_approved:
            raise AppException(message=MESSAGE.CANNOT_UPDATE_APPROVED_SHIFT, status_code=HTTPStatus.BAD_REQUEST)

            # Prevents overlapping shifts for the same user
        conflicting_shift = None
        if update_data.start_time or update_data.end_time:
            start_time = update_data.start_time or existing_shift.start_time
            end_time = update_data.end_time or existing_shift.end_time

            conflicting_shift = db.exec(
                select(Shift).where(
                    (Shift.user_id == user_id) &
                    (Shift.id != shift_id) &
                    (Shift.start_time < end_time) &
                    (Shift.end_time > start_time)
                )
            ).first()

        if conflicting_shift:
            raise AppException(
                message=MESSAGE.SHIFT_TIME_CONFLICT,
                status_code=HTTPStatus.CONFLICT
            )

        # Update shift fields
        update_data = update_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(existing_shift, key, value)

        # Always update the updated_at timestamp
        existing_shift.updated_at = datetime.now()

        try:
            db.add(existing_shift)
            db.commit()
            db.refresh(existing_shift)

            return ShiftResponse(success=True, data=existing_shift, message=MESSAGE.UPDATED)
        except Exception as e:
            db.rollback()
            raise AppException(message=f"Error updating shift: {str(e)}", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


    @staticmethod
    async def delete_shift(db: Session, user_id: uuid.UUID, shift_id: uuid.UUID):
        query = select(Shift).where((Shift.user_id == user_id) & (Shift.id == shift_id))
        shift = db.exec(query).first()

        if not shift:
            raise NotFoundException(MESSAGE.SHIFT_NOT_FOUND)

        try:
            db.delete(shift)
            db.commit()
        except Exception as e:
            db.rollback()
            raise AppException(message=f"Error deleting shift: {str(e)}", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

        return ShiftDeleteResponse()
