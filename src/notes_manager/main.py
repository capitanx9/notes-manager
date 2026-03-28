from fastapi import FastAPI

from src.notes_manager.config import get_settings
from src.notes_manager.database import engine
from src.notes_manager.models import User, Article

app = FastAPI()
settings = get_settings()

@app.get("/liveness")
def liveness():
    return {"status": "ok"}
