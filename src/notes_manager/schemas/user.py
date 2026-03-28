from datetime import datetime

from pydantic import BaseModel

# =============================================================================
#  Request
# =============================================================================


class UserUpdate(BaseModel):
    email: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    role: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "newemail@example.com",
                    "first_name": "Updated",
                    "last_name": "Name",
                }
            ]
        }
    }

# =============================================================================
#  Response
# =============================================================================


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: str | None
    last_name: str | None
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int