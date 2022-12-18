from models.file import models_file

from sqlalchemy.orm import Session


def load_file(filename: str, content: bytes, db: Session):
    db_file = models_file.File(filename=filename, content=content)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file.id


def get_file(id: int, db: Session):
    return (
        db.query(models_file.File.content).filter(models_file.File.id == id).first()
    )


# def get_files(db: Session):
#     return db.query(models.File)
