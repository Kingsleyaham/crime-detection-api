from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import Session

from app.api.dependencies import CurrentUserDep
from app.api.services.auth_service import CurrentUserToken
from app.api.services.notification_service import NotificationService
from app.core.database import get_session
from app.schemas.notification import NotificationsResponse, NotificationResponse, NotificationDeleteResponse

router = APIRouter()


@router.get("/", response_model=NotificationsResponse, status_code=200)
async def get_notifications(current_user: CurrentUserDep, token: CurrentUserToken, db: Session = Depends(get_session)):
    return await NotificationService.get_notifications(current_user.id, db)


@router.get("/{notification_id}", response_model=NotificationResponse, status_code=200)
async def get_notification(notification_id: UUID, current_user: CurrentUserDep, token: CurrentUserToken,
                           db: Session = Depends(get_session)):
    return await NotificationService.get_notification(notification_id, db, current_user.id)


@router.delete("/{notification_id}", response_model=NotificationDeleteResponse, status_code=200)
async def delete_notification(notification_id: UUID, current_user: CurrentUserDep, token: CurrentUserToken,
                              db: Session = Depends(get_session)):
    return await NotificationService.delete_notification(notification_id, db, current_user.id)

@router.delete("/all", response_model=NotificationDeleteResponse, status_code=200)
async def delete_all_notifications(current_user: CurrentUserDep, token: CurrentUserToken, db: Session = Depends(get_session)):
    return await NotificationService.delete_all_notifications(current_user.id, db)


@router.patch("/{notification_id}/mark-read", response_model=NotificationResponse, status_code=200)
async def mark_notification_read(notification_id: UUID, current_user: CurrentUserDep, token: CurrentUserToken, db: Session = Depends(get_session)):
    return  await NotificationService.mark_notification_as_read(notification_id, db, current_user.id)