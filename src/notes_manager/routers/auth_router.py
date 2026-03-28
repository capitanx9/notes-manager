from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.notes_manager.dependencies.database import get_db
from src.notes_manager.schemas.auth import LoginRequest, TokenResponse
from src.notes_manager.services.auth_service import authenticate_user, create_access_token

router = APIRouter()


@router.post("/login", response_model=TokenResponse, summary="Login", description="Authenticate with email and password to receive a JWT token.")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    token = create_access_token(user.id, user.role.value)
    return TokenResponse(access_token=token)
