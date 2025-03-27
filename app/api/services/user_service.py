from sqlmodel import Session, select

from app.constants.messages import MESSAGE
from app.core.exceptions import UserAlreadyExists
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, SignupResponse
from app.utils.password import get_password_hash


class UserService:
    @staticmethod
    async def create_user(db: Session, user_data: UserCreate):
        # Check if the user already exists
        existing_user = await UserService.get_user_by_email(db, str(user_data.email))
        if existing_user:
            raise UserAlreadyExists()

        hashed_password = get_password_hash(user_data.password)

        user = User(email=user_data.email, password=hashed_password, role=user_data.role, firstname=user_data.firstname,
                    lastname=user_data.lastname, phone=user_data.phone)
        # save to database
        db.add(user)
        db.commit()
        db.refresh(user)

        # return UserResponse.model_validate(user)
        return SignupResponse(
            user=user,
            message=MESSAGE.USER_CREATED
        )

    @staticmethod
    async def get_user_by_email(db: Session, email: str) -> User:
        return db.exec(select(User).where(User.email == email)).first()
