from datetime import datetime

from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import db_sidekick
from apps.user.auth.dependencies import get_access_token_payload
from apps.user.auth.services import AuthService
from apps.user.dependencies import get_current_user
from apps.user.messages import UserResponseMessage
from apps.user.schemas import UserCreate, UserResponse, UserSchema, UserUpdate
from apps.user.services import UserService
from apps.user.auth import auth_router

router: APIRouter = APIRouter(prefix="/user", tags=["User"])
router.include_router(auth_router)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_new_user(
    user: UserCreate,
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> UserSchema:
    """New user registration"""
    return await UserService.register_new_user(session, user)


@router.get("/me")
async def get_current_user(
    payload: dict = Depends(get_access_token_payload),
    current_user: UserSchema = Depends(get_current_user),
) -> UserResponse:
    iat: int = payload.get("iat")
    login_at: str = datetime.fromtimestamp(iat).strftime("%d %B %Y")
    user_response: UserResponse = UserResponse(
        login_at=login_at, **current_user.model_dump()
    )
    return user_response


@router.put("/me")
async def update_current_user(
    user_data: UserUpdate,
    current_user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> UserSchema:
    return await UserService.update_user(session, current_user.id, user_data)


@router.delete("/me")
async def delete_current_user(
    request: Request,
    response: Response,
    current_user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(db_sidekick.session_getter),
) -> dict[str, str]:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    await AuthService.logout(session, request.cookies.get("refresh_token"))
    await UserService.delete_user(session, current_user.id)
    return UserResponseMessage.INACTIVE_STATUS
