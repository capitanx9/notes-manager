from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.notes_manager.models.article import Article

# =============================================================================
#  Read
# =============================================================================


def get_by_id(db: Session, article_id: int) -> Article | None:
    return db.query(Article).filter(Article.id == article_id).first()


def get_list(
    db: Session, limit: int, offset: int, search: str | None = None
) -> tuple[list[Article], int]:
    query = db.query(Article)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Article.title.ilike(pattern),
                Article.content.ilike(pattern),
                Article.summary.ilike(pattern),
            )
        )
    total = query.count()
    items = query.order_by(Article.created_at.desc()).offset(offset).limit(limit).all()
    return items, total

# =============================================================================
#  Create
# =============================================================================


def create(
    db: Session,
    title: str,
    content: str,
    owner_id: int,
    summary: str | None = None,
    status: str = "draft",
) -> Article:
    article = Article(
        title=title,
        content=content,
        summary=summary,
        status=status,
        owner_id=owner_id,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

# =============================================================================
#  Update
# =============================================================================


def update(db: Session, article: Article, data: dict) -> Article:
    for key, value in data.items():
        if value is not None:
            setattr(article, key, value)
    db.commit()
    db.refresh(article)
    return article

# =============================================================================
#  Delete
# =============================================================================


def delete(db: Session, article: Article) -> None:
    db.delete(article)
    db.commit()
