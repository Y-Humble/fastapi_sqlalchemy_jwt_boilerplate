from typing import Annotated
from uuid import UUID

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict, EmailStr

from apps.user.models import Status


class UserBase(BaseModel):
    username: Annotated[str, MaxLen(32)]
    email: EmailStr | None = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    username: Annotated[str, MaxLen(32)] | None = None
    password: str | None = None


class UserPartialUpdate(UserUpdate):
    pass


class UserSchema(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    active: bool
    status: Status


class UserCreateDB(UserBase):
    hashed_password: bytes


class UserUpdateDB(UserBase):
    hashed_password: bytes | None = None


class UserPartialUpdateDB(UserUpdateDB):
    username: Annotated[str, MaxLen(32)] | None = None


class UserResponse(UserSchema):
    login_at: str
