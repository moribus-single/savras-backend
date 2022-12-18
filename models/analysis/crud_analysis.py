from models.analysis import models_analysis
import json
from sqlalchemy.orm import Session


def save_result(fileid: int, result: dict, db: Session):
    """Сохранение результата линейной регрессии"""
    db_file = models_analysis.LinearReg(
        fileid=fileid,
        x_cord_first=result["x_cord_first"],
        x_cord_second=result["x_cord_second"],
        y_cord_first=result["y_cord_first"],
        y_cord_second=result["y_cord_second"],
        model_score=result["model_score"]
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)


def get_result(fileid: int, db: Session):
    """Выдача результата линейной регрессии"""
    return db.query(models_analysis.LinearReg.result).filter(models_analysis.LinearReg.fileid == fileid).first()


# def get_files(db: Session):
#     return db.query(models.File)
