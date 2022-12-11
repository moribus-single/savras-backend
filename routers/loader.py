from fastapi import APIRouter, UploadFile, File, Depends
from services.loader import LoaderService
from sqlalchemy.orm import Session
from core.database import get_db

# will be included into the app
router = APIRouter()
# provides functions for loader
loader = LoaderService()


@router.get('loadCsv/{filename}&{content}', tags=['loader'])
async def load_csv(file: UploadFile = File(), db: Session = Depends(get_db)):
    loader.load_csv(file.filename, await file.read(), db)


@router.post("/loadXlsx/", tags=['loader'])
async def load_xlsx(file: UploadFile = File(), db: Session = Depends(get_db)):
    fileid = loader.load_xlsx(file.filename, await file.read(), db)
    return {
        'fileid': fileid,
    }
