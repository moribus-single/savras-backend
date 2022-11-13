from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from user import schemas
from services.auth import AuthenticationService
from core.database import get_db

auth = AuthenticationService()

router = APIRouter()


@router.post("/login/", tags=["auth"])
async def login(user: schemas.UserBase, db: Session = Depends(get_db)):
    return auth.login(user, db)


@router.post("/register/", tags=["auth"])
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth.register(user, db)
