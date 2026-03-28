from datetime import datetime

from pydantic import BaseModel

# =============================================================================
#  Request
# =============================================================================


class ArticleCreate(BaseModel):
    title: str
    content: str
    summary: str | None = None
    status: str = "draft"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "My New Article",
                    "content": "This is the full content of my article.",
                    "summary": "A brief summary",
                    "status": "published",
                }
            ]
        }
    }


class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    summary: str | None = None
    status: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Updated Title",
                    "content": "Updated content.",
                }
            ]
        }
    }

# =============================================================================
#  Response
# =============================================================================


class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    summary: str | None
    status: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ArticleListResponse(BaseModel):
    items: list[ArticleResponse]
    total: int
