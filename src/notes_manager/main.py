from fastapi import FastAPI

from src.notes_manager.config import get_settings
from src.notes_manager.routers.auth_router import router as auth_router
from src.notes_manager.routers.article_router import router as article_router
from src.notes_manager.routers.user_router import router as user_router

app = FastAPI(
    title="Notes Manager API",
    description="REST API for managing users and articles with role-based access control.",
    version="1.0.0",
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(article_router, prefix="/articles", tags=["Articles"])
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/liveness", tags=["Health"], summary="Health check", description="Returns OK if the service is running.")
def liveness():
    return {"status": "ok"}
