from sqlalchemy.orm import Session
from fastapi import HTTPException

from user import schemas, crud


class AuthenticationService:

    @staticmethod
    def login(user: schemas.UserBase, db: Session):
        return user

    @staticmethod
    def register(user: schemas.UserCreate, db: Session):
        db_user = crud.get_user(email=user.email, db=db)
        if db_user:
            return HTTPException(status_code=400, detail="Already registered")
        return crud.create_user(user=user, db=db)
