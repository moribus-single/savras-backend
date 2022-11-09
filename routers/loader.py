from fastapi import APIRouter
from services.loader import LoaderService

# will be included into the app
router = APIRouter()
# provides functions for loader
loader = LoaderService()


@router.get("loadCsv/{path}", tags=['loader'])
async def load_csv(path: str):
    loader.load_csv(path)


@router.get("loadXlsx/{path}", tags=['loader'])
async def load_xlsx(path: str):
    loader.load_xlsx(path)
