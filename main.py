from fastapi import FastAPI

from core.router import get_all_routers

app = FastAPI()

app.include_router(get_all_routers())
