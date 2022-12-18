from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.auth import AuthenticationService
from core.database import get_db
from services.linear_regression import LinearRegres as lr


auth = AuthenticationService()

router = APIRouter()


@router.post("/linReg/", tags=["linear_regression"])
async def lin_reg(fileid: int, db: Session = Depends(get_db)):
    """Эндпоинт линейной регрессии"""
    return lr().make_df(fileid, db)


@router.get("/linReg/", tags=["linear_regression"])
async def get_res(fileid: int, db: Session = Depends(get_db)):
    """Эндпоинт возвращающий результат линейной регрессии"""
    return lr().get_result(fileid, db)
