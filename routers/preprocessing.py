from fastapi import APIRouter
from services.preprocessor import Preprocessor

# will be included into the app
router = APIRouter()
# provides functions for preprocessing
preprocessor = Preprocessor()


@router.get("preprocess", tags=['preprocessor'])
async def select_method(method: str):
    match method:
        case 'method_one':
            preprocessor.method_one()
        case 'method_two':
            preprocessor.method_two()
