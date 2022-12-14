from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.auth import AuthenticationService
from core.database import get_db
from services.linear_regression import LinearRegres as lr
from services.anomaly import Anomaly
from services.prediction import Prediction
from services.prediction_neural import PredictionNeural
from fastapi.responses import FileResponse


auth = AuthenticationService()

router = APIRouter()


@router.post("/linReg/", tags=["linear_regression"])
async def lin_reg(fileid: int, db: Session = Depends(get_db)):
    """Эндпоинт линейной регрессии."""
    return lr().make_df(fileid, db)


@router.get("/linReg/", tags=["linear_regression"])
async def get_res(fileid: int, db: Session = Depends(get_db)):
    """Эндпоинт, возвращающий результат линейной регрессии."""
    return lr().get_result(fileid, db)


@router.post("/anomaly/", tags=["anomaly"])
async def post_anomaly(fileid: int, with_anomaly_bool: bool, db: Session = Depends(get_db)):
    """Эндпоинт поиска аномалий."""
    filename = Anomaly().make_df(fileid, with_anomaly_bool, db)
    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename,
    )


@router.get("/anomaly/", tags=["anomaly"])
async def get_anomaly(fileid: int, with_anomaly_bool: bool, db: Session = Depends(get_db)):
    """Эндпоинт, возвращающий результат поиска аномалий."""
    filename = Anomaly().get_result(fileid,with_anomaly_bool, db)
    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return FileResponse(
        filename,
        media_type=media_type,
        filename=filename,
    )

@router.post("/prediction/", tags=["prediction"])
async def post_prediction(fileid: int, predictions: int, db: Session = Depends(get_db)):
    """Эндпоинт обычного прогнозирования."""
    filename = Prediction().make_df(fileid, predictions, db)
    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename,
    )


@router.get("/prediction/", tags=["prediction"])
async def get_prediction(fileid: int, db: Session = Depends(get_db)):
    """Эндпоинт, возвращающий результат обычного прогнозирования."""
    filename = Prediction().get_result(fileid, db)
    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return FileResponse(
        filename,
        media_type=media_type,
        filename=filename,
    )

@router.post("/prediction_neural/", tags=["prediction_neural"])
async def post_prediction_neural(fileid: int, predictions: int, db: Session = Depends(get_db)):
    """Эндпоинт нейронного прогнозирования."""
    filename = PredictionNeural().make_df(fileid, predictions, db)
    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename,
    )


@router.get("/prediction_neural/", tags=["prediction_neural"])
async def get_prediction_neural(fileid: int, db: Session = Depends(get_db)):
    """Эндпоинт, возвращающий результат нейронного прогнозирования."""
    filename = PredictionNeural().get_result(fileid, db)
    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return FileResponse(
        filename,
        media_type=media_type,
        filename=filename,
    )