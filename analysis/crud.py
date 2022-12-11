from analysis import models
import json
from sqlalchemy.orm import Session

def save_result(fileid: int, result: dict, db: Session):
    """Сохранение результата линейной регрессии"""
    result = json.dumps(result)
    db_file = models.LinearReg(fileid = fileid, result=result)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)


def get_result(fileid: int, db: Session):
    """Выдача результата линейной регрессии"""
    return db.query(models.LinearReg.result).filter(models.LinearReg.fileid == fileid).first()


# def get_files(db: Session):
#     return db.query(models.File)
