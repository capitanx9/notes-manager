from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.notes_manager.dependencies.auth import get_current_user
from src.notes_manager.dependencies.database import get_db
from src.notes_manager.models.user import User
from src.notes_manager.schemas.user import (
    UserListResponse,
    UserResponse,
    UserUpdate,
)
from src.notes_manager.services import user_service

router = APIRouter()

# =============================================================================
#  Me
# =============================================================================


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get the profile of the currently authenticated user.",
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return user_service.get_me(current_user)

# =============================================================================
#  List
# =============================================================================


@router.get(
    "",
    response_model=UserListResponse,
    summary="List users",
    description="Get a paginated list of users. Admin only. Supports search by email, username, first and last name.",
)
def list_users(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = user_service.list_users(db, limit, offset, search, current_user)
    return UserListResponse(items=items, total=total)

# =============================================================================
#  Get by ID
# =============================================================================


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Get a single user by ID. Admin only.",
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_service.get_user(db, user_id, current_user)

# =============================================================================
#  Update
# =============================================================================


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update a user profile. Users can only update themselves. Admins can update anyone. Only admins can change roles.",
)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_service.update_user(
        db, user_id, data.model_dump(exclude_unset=True), current_user
    )

# =============================================================================
#  Delete
# =============================================================================


@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Delete user",
    description="Delete a user. Admin only. Cannot delete yourself.",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service.delete_user(db, user_id, current_user)
