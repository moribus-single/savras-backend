from fastapi import APIRouter

from routers import auth, loader, analysis

router = APIRouter()


def get_all_routers():
    """
    Подключение всех роутеров в один
    """

    router.include_router(auth.router)
    router.include_router(loader.router)
    router.include_router(analysis.router)
    return router
