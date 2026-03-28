from fastapi import FastAPI

from src.notes_manager.config import get_settings
from src.notes_manager.database import engine
from src.notes_manager.models import User, Article
from src.notes_manager.routers.auth_router import router as auth_router

app = FastAPI()
settings = get_settings()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])


@app.get("/liveness")
def liveness():
    return {"status": "ok"}
