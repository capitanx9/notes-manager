import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from src.notes_manager.database import Base


class ArticleStatus(str, enum.Enum):
    draft = "draft"
    published = "published"


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(String, nullable=True)
    status = Column(Enum(ArticleStatus), nullable=False, default=ArticleStatus.draft)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", backref="articles")
