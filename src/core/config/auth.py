from pydantic import BaseModel


class AuthSettings(BaseModel):
    algorithm: str
    token_type_field: str
    token_url: str
    access_token_type: str
    refresh_token_type: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int = 60 * 24 * 30
