from models.analysis import models_analysis as models
import json
from sqlalchemy.orm import Session


def save_result_lr(fileid: int, result: dict, db: Session):
    """Сохранение результата линейной регрессии"""
    result = json.dumps(result)
    db_file = models.LinearReg(fileid=fileid, result=result)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)


def get_result_lr(fileid: int, db: Session):
    """Выдача результата линейной регрессии"""
    return (
        db.query(models.LinearReg.result)
        .filter(models.LinearReg.fileid == fileid)
        .first()
    )


def save_result_anom(
    fileid: int, with_anomaly: bytes, without_anomaly: bytes, db: Session
):
    db_file = models.Anomaly(
        fileid=fileid, with_anomaly=with_anomaly, without_anomaly=without_anomaly
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file.id


def get_result_anom(fileid: int, db: Session):
    return (
        db.query(models.Anomaly.result).filter(models.Anomaly.fileid == fileid).first()
    )


# def get_files(db: Session):
#     return db.query(models.File)
