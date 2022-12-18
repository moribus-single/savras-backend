from user import models, schemas

from sqlalchemy.orm import Session


def create_user(user: schemas.UserInDB, db: Session):
    """Создание пользователя в бд."""

    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(username: str, db: Session) -> models.User:
    """Получение пользователя по username из бд."""

    return db.query(models.User).filter(models.User.username == username).first()
