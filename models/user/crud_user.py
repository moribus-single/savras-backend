from models.user import models_user, schemas_user

from sqlalchemy.orm import Session


def create_user(user: schemas_user.UserInDB, db: Session):
    """Создание пользователя в бд."""

    db_user = models_user.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(username: str, db: Session) -> models_user.User:
    """Получение пользователя по username из бд."""

    return db.query(models_user.User).filter(models_user.User.username == username).first()
