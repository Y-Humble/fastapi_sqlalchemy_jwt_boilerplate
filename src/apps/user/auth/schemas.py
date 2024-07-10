from pydantic import BaseModel
from uuid import UUID


class RefreshSessionCreate(BaseModel):
    refresh_token: str
    expires_in: int
    user_id: UUID


class RefreshSessionUpdate(BaseModel):
    user_id: UUID | None = None


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    scheme: str = "Bearer"
