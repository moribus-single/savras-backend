from fastapi import APIRouter
from sqlalchemy.orm import Session

from user.schemas import UserBase
from services.auth import AuthenticationService

auth = AuthenticationService()

router = APIRouter()


@router.post("/login/", tags=["auth"])
async def login(user: UserBase, db: Session):
    auth.login(user, db)


@router.post("/register/", tags=["auth"])
async def register(user: UserBase, db: Session):
    auth.register(user, db)
