from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from decouple import config

from core.Exeptions import IncorrectDataException
from models.user import schemas_user as schemas
from models.user import crud_user as crud

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))


class AuthenticationService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def login(self, form_data: schemas.UserInDB, db: Session):
        """Авторизация пользователя."""
        user = self.authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise IncorrectDataException
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def register(self, user: schemas.UserInDB, db: Session):
        """Регистрация пользователя."""
        db_user = crud.get_user(username=user.username, db=db)
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already registered")
        user.password = self.get_password_hash(user.password)
        return crud.create_user(user=user, db=db)

    def verify_password(self, password, hashed_password):
        """Проверка полученного пароля."""
        return self.pwd_context.verify(password, hashed_password)

    def get_password_hash(self, password):
        """Получение хеша пароля."""
        return self.pwd_context.hash(password)

    def authenticate_user(self, username: str, password: str, db: Session):
        """Проверка введенных данных и получение пользователя."""
        user = crud.get_user(username, db)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):  
        """Создание токена."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
