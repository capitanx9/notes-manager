from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.notes_manager.models.user import User
from src.notes_manager.repositories import user_repository

# =============================================================================
#  Read
# =============================================================================


def get_me(current_user: User) -> User:
    return current_user


def get_user(db: Session, user_id: int, current_user: User) -> User:
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view other users",
        )
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


def list_users(
    db: Session, limit: int, offset: int, search: str | None, current_user: User
) -> tuple[list[User], int]:
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can list users",
        )
    return user_repository.get_list(db, limit, offset, search)

# =============================================================================
#  Update
# =============================================================================


def update_user(
    db: Session, user_id: int, data: dict, current_user: User
) -> User:
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    role = current_user.role.value

    if role != "admin" and user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile",
        )

    if "role" in data and data["role"] is not None and role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change roles",
        )

    return user_repository.update(db, user, data)

# =============================================================================
#  Delete
# =============================================================================


def delete_user(db: Session, user_id: int, current_user: User) -> None:
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete users",
        )

    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself",
        )

    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user_repository.delete(db, user)
