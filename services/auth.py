from user.schemas import UserBase
from sqlalchemy.orm import Session


class AuthenticationService:

    @staticmethod
    def login(user: UserBase, db: Session):
        return user

    @staticmethod
    def register(user: UserBase, db: Session):
        return user
