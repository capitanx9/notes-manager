from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.notes_manager.dependencies.auth import get_current_user
from src.notes_manager.dependencies.database import get_db
from src.notes_manager.models.user import User
from src.notes_manager.schemas.article import (
    ArticleCreate,
    ArticleListResponse,
    ArticleResponse,
    ArticleUpdate,
)
from src.notes_manager.services import article_service

router = APIRouter()

# =============================================================================
#  List
# =============================================================================


@router.get(
    "",
    response_model=ArticleListResponse,
    summary="List articles",
    description="Get a paginated list of articles. Supports search by title, content and summary.",
)
def list_articles(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = article_service.list_articles(db, limit, offset, search)
    return ArticleListResponse(items=items, total=total)

# =============================================================================
#  Get by ID
# =============================================================================


@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
    summary="Get article by ID",
    description="Get a single article by its ID.",
)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return article_service.get_article(db, article_id)

# =============================================================================
#  Create
# =============================================================================


@router.post(
    "",
    response_model=ArticleResponse,
    status_code=201,
    summary="Create article",
    description="Create a new article. The owner is set automatically from the authenticated user.",
)
def create_article(
    data: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return article_service.create_article(db, data.model_dump(), current_user)

# =============================================================================
#  Update
# =============================================================================


@router.put(
    "/{article_id}",
    response_model=ArticleResponse,
    summary="Update article",
    description="Update an article. Users can only update their own articles. Editors and admins can update any article.",
)
def update_article(
    article_id: int,
    data: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return article_service.update_article(
        db, article_id, data.model_dump(exclude_unset=True), current_user
    )

# =============================================================================
#  Delete
# =============================================================================


@router.delete(
    "/{article_id}",
    status_code=204,
    summary="Delete article",
    description="Delete an article. Users can only delete their own articles. Admins can delete any article. Editors cannot delete.",
)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    article_service.delete_article(db, article_id, current_user)
