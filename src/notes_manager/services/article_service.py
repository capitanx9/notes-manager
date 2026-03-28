from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.notes_manager.models.article import Article
from src.notes_manager.models.user import User
from src.notes_manager.repositories import article_repository

# =============================================================================
#  Read
# =============================================================================


def get_article(db: Session, article_id: int) -> Article:
    article = article_repository.get_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    return article


def list_articles(
    db: Session, limit: int, offset: int, search: str | None = None
) -> tuple[list[Article], int]:
    return article_repository.get_list(db, limit, offset, search)

# =============================================================================
#  Create
# =============================================================================


def create_article(db: Session, data: dict, current_user: User) -> Article:
    return article_repository.create(
        db,
        title=data["title"],
        content=data["content"],
        summary=data.get("summary"),
        status=data.get("status", "draft"),
        owner_id=current_user.id,
    )

# =============================================================================
#  Update
# =============================================================================


def update_article(
    db: Session, article_id: int, data: dict, current_user: User
) -> Article:
    article = get_article(db, article_id)
    role = current_user.role.value

    if role == "user" and article.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own articles",
        )

    return article_repository.update(db, article, data)

# =============================================================================
#  Delete
# =============================================================================


def delete_article(db: Session, article_id: int, current_user: User) -> None:
    article = get_article(db, article_id)
    role = current_user.role.value

    if role == "editor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Editors cannot delete articles",
        )

    if role == "user" and article.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own articles",
        )

    article_repository.delete(db, article)
