from file import models

from sqlalchemy.orm import Session


def load_file(filename: str, content: bytes, db: Session):
    db_file = models.File(filename=filename, content=content)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)


def get_file(id: int, db: Session):
    return db.query(models.File).filter(models.File.id == id).first()


# def get_files(db: Session):
#     return db.query(models.File)
