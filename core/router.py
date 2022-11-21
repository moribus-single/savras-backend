from fastapi import APIRouter

from routers import auth, loader

router = APIRouter()


def get_all_routers():
    """
    Подключение всех роутеров в один
    """

    router.include_router(auth.router)
    router.include_router(loader.router)
    return router
