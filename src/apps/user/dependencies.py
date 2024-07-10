from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import db_sidekick
from apps.user import Status
from apps.user.auth.dependencies import (
    get_access_token_payload,
    get_refresh_token_payload,
)
from apps.user.auth.exceptions import InvalidTokenException
from apps.user.exceptions import AccessIsDeniedException, InactiveUserException
from apps.user.repositories import UserRepo
from apps.user.schemas import UserSchema
from apps.user.utils import validate_token_type


async def get_user_by_sub(session: AsyncSession, payload: dict) -> UserSchema:
    user_id: int | None = payload.get("sub")
    if user := await UserRepo.get_one_or_none(session, id=user_id):
        return UserSchema.model_validate(user)
    raise InvalidTokenException


async def get_current_auth_user(
    payload: dict = Depends(get_access_token_payload),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> UserSchema:
    validate_token_type(payload, settings.auth.access_token_type)
    return await get_user_by_sub(session, payload)


async def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_refresh_token_payload),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> UserSchema:
    validate_token_type(payload, settings.auth.refresh_token_type)
    return await get_user_by_sub(session, payload)


def get_current_active_user(
    user: UserSchema = Depends(get_current_auth_user),
) -> UserSchema:
    if user.active:
        return user
    raise InactiveUserException


def get_current_user(
    user: UserSchema = Depends(get_current_active_user),
) -> UserSchema:
    if user.status != Status.BANNED:
        return user
    logger.warning(f"Wrong status - {user.status} == {Status.BANNED}")
    raise AccessIsDeniedException


def get_user_admin(user: UserSchema = Depends(get_current_user)) -> UserSchema:
    if user.status == Status.ADMIN:
        return user
    logger.warning(f"Wrong status - {user.status} != {Status.ADMIN}")
    raise AccessIsDeniedException
