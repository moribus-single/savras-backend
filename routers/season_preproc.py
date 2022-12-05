from fastapi import APIRouter
from services.season_preprocessor import SeasonPreprocessor

router = APIRouter()

# will be included into the app
router = APIRouter()
# provides functions for preprocessing
preprocessor = SeasonPreprocessor()


@router.get("season_preprocess", tags=['season_preprocessor'])
async def process():
    preprocessor.process()
