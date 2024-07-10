from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import db_sidekick
from apps.user.auth.messages import AuthResponseMessage
from apps.user.auth.schemas import TokenInfo
from apps.user.auth.services import AuthService
from apps.user.dependencies import (
    get_current_active_user,
    get_current_auth_user_for_refresh,
)
from apps.user.exceptions import InvalidCredentialsException
from apps.user.schemas import UserSchema
from apps.user.services import UserService

router: APIRouter = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
    response: Response,
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> TokenInfo:
    """
    Authenticate user, issue access and refresh tokens,
    save access and refresh tokens in cookie
    :return: TokenInfo(
        access_token: str,
        refresh_token: str,
        token_type: str = "Bearer"
    )
    """
    if user := await UserService.authenticate_user(
        session,
        credentials.password,
        credentials.username,
    ):
        token: TokenInfo = await AuthService.issue_auth_token(session, user)
        AuthService.set_token_and_schema_in_cookies(
            response,
            settings.auth.access_token_type,
            token.access_token,
            token.scheme,
            settings.auth.access_token_expire_minutes * 60,
        )
        AuthService.set_token_and_schema_in_cookies(
            response,
            settings.auth.refresh_token_type,
            token.refresh_token,
            token.scheme,
            settings.auth.refresh_token_expire_minutes * 60,
        )
        return token

    raise InvalidCredentialsException


@router.delete("/logout")
async def logout(
    request: Request,
    response: Response,
    user: UserSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> dict[str, str]:
    """
    Logout User
    """
    response.delete_cookie(settings.auth.access_token_type)
    response.delete_cookie(settings.auth.refresh_token_type)

    await AuthService.logout(
        session, request.cookies.get(settings.auth.refresh_token_type)
    )
    return AuthResponseMessage.LOGOUT


@router.post(
    "/refresh", response_model=TokenInfo, response_model_exclude_none=True
)
async def refresh_token(
    request: Request,
    response: Response,
    user: UserSchema = Depends(get_current_auth_user_for_refresh),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> TokenInfo:
    """
    Create new access token by refresh token,
    update access token in cookie
    :return: TokenInfo(
        access_token: str,
        token_type: str = "Bearer"
    )
    """
    new_token: TokenInfo = await AuthService.refresh_token(
        session,
        request.cookies.get(settings.auth.refresh_token_type),
    )
    AuthService.set_token_and_schema_in_cookies(
        response,
        settings.auth.access_token_type,
        new_token.access_token,
        new_token.scheme,
        max_age=settings.auth.access_token_expire_minutes * 60,
    )
    return new_token


@router.delete("/abort")
async def abort_all_sessions(
    response: Response,
    user: UserSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> dict[str, str]:
    response.delete_cookie(settings.auth.access_token_type)
    response.delete_cookie(settings.auth.refresh_token_type)

    await AuthService.abort_all_sessions(session, user.id)
    return AuthResponseMessage.ABORT
