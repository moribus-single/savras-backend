from fastapi import FastAPI

from core.router import get_all_routers
from core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(get_all_routers())
