from fastapi import APIRouter
from services.manager import Manager

# will be included into the app
router = APIRouter()
# provides functions for preprocessing
manager = Manager()


@router.get("setOrder", tags=['manager'])
async def set_order():
    manager.set_order()


@router.get("saveToFile", tags=['manager'])
async def save_to_file():
    manager.save_to_file()


@router.get("updateFromFile", tags=['manager'])
async def update_from_file():
    manager.update_from_file()
