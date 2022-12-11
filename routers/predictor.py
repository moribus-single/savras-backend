from fastapi import APIRouter
from services.predictor import Predictor

# will be included into the app
router = APIRouter()
# provides functions for prediction
predictor = Predictor()


@router.get("predict", tags=['predictor'])
async def predict():
    predictor.predict()
