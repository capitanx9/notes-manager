from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.notes_manager.models.user import User

# =============================================================================
#  Read
# =============================================================================


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_list(
    db: Session, limit: int, offset: int, search: str | None = None
) -> tuple[list[User], int]:
    query = db.query(User)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                User.email.ilike(pattern),
                User.username.ilike(pattern),
                User.first_name.ilike(pattern),
                User.last_name.ilike(pattern),
            )
        )
    total = query.count()
    items = query.order_by(User.created_at.desc()).offset(offset).limit(limit).all()
    return items, total

# =============================================================================
#  Update
# =============================================================================


def update(db: Session, user: User, data: dict) -> User:
    for key, value in data.items():
        if value is not None:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# =============================================================================
#  Delete
# =============================================================================


def delete(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
