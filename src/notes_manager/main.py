from fastapi import FastAPI

from src.notes_manager.config import get_settings
from src.notes_manager.routers.auth_router import router as auth_router
from src.notes_manager.routers.article_router import router as article_router
from src.notes_manager.routers.user_router import router as user_router

app = FastAPI()
settings = get_settings()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(article_router, prefix="/articles", tags=["Articles"])
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/liveness")
def liveness():
    return {"status": "ok"}
