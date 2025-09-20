from fastapi import FastAPI

from app.api import items

app = FastAPI()

app.include_router(items.router, prefix="/api", tags=["items"])