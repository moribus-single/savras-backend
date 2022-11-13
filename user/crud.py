from user import models, schemas

from sqlalchemy.orm import Session


def create_user(user: schemas.UserCreate, db: Session):
    """
    Создание пользователя в бд
    """

    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(email: str, db: Session):
    """
    Получение пользователя по email из бд
    """

    return db.query(models.User).filter(models.User.email == email).first()
