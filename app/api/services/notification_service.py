from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select, delete

from app.constants.messages import MESSAGE
from app.core.exceptions import NotFoundException
from app.models.notification import Notification
from app.schemas.notification import NotificationCreateResponse, NotificationCreate, NotificationsResponse, \
    NotificationResponse, NotificationDeleteResponse


class NotificationService:
    @staticmethod
    async def _find_by_id(id: UUID, db: Session):
        query = select(Notification).where(Notification.id == id)
        notification = db.exec(query).first()

        if not notification:
            raise NotFoundException(message=MESSAGE.NOTIFICATION_NOT_FOUND)

        return notification

    @staticmethod
    async def create_notification(data: NotificationCreate, db: Session) -> NotificationCreateResponse:
        data = data.model_dump()
        notification = Notification(**data)

        # save to database
        db.add(notification)
        db.commit()
        db.refresh(notification)

        return NotificationCreateResponse()

    @staticmethod
    async def get_notifications(user_id: str, db: Session) -> NotificationsResponse:
        query = select(Notification).where(Notification.user_id == user_id)
        results = db.exec(query).all()

        return NotificationsResponse(data=results)

    @staticmethod
    async def get_notification(notification_id: UUID, db: Session, user_id: UUID):
        notification = await NotificationService._find_by_id(notification_id, db)

        if not notification.user_id == user_id:
            raise NotFoundException(message=MESSAGE.NOTIFICATION_NOT_FOUND)

        return NotificationResponse(data=notification)

    @staticmethod
    async def delete_notification(notification_id: UUID, db: Session, user_id: UUID):
        notification = await NotificationService._find_by_id(notification_id, db)

        if not notification.user_id == user_id:
            raise NotFoundException(message=MESSAGE.NOTIFICATION_NOT_FOUND)

        try:
            db.delete(notification)
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Error deleting notification: {str(e)}")

    @staticmethod
    async def delete_all_notifications(user_id: UUID, db: Session):
        try:
            query = delete(Notification).where(Notification.user_id == user_id)
            db.exec(query)
            db.commit()

            return NotificationDeleteResponse()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error deleting all notifications: {str(e)}")

    @staticmethod
    async def mark_notification_as_read(notification_id: UUID, db: Session, user_id: UUID):
        try:
            notification = await NotificationService._find_by_id(notification_id, db)

            if not notification.user_id == user_id:
                raise NotFoundException(message=MESSAGE.NOTIFICATION_NOT_FOUND)

            notification.is_read = True
            db.add(notification)
            db.commit()
            db.refresh(notification)

            NotificationResponse(data=notification, message=MESSAGE.NOTIFICATION_MARKED_AS_READ)
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error marking notification as read: {str(e)}")
