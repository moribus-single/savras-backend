from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.user import schemas_user as schemas
from Token.schemas import Token
from services.auth import AuthenticationService
from core.database import get_db

auth = AuthenticationService()

router = APIRouter()


@router.post("/login/", tags=["auth"], response_model=Token)
async def login(*, form_data: schemas.UserInDB, db: Session = Depends(get_db)):
    return auth.login(form_data, db)


@router.post("/register/", tags=["auth"])
async def register(user: schemas.UserInDB, db: Session = Depends(get_db)):
    return auth.register(user, db)
