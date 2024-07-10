import jwt
from datetime import UTC, datetime, timedelta
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from core.config import settings
from core.constants import Const
from apps.user.auth.exceptions import InvalidTokenException
from apps.user.auth.repositories import RefreshSessionRepo
from apps.user.auth.schemas import TokenInfo
from apps.user.repositories import UserRepo
from apps.user.schemas import UserSchema


class AuthService:
    @classmethod
    async def issue_auth_token(
        cls,
        session: AsyncSession,
        user: UserSchema,
    ) -> TokenInfo:
        """
        Issue access and refresh tokens then save refresh token into database
        :return: TokenInfo(
            access_token: str,
            refresh_token: str,
            token_type: str = "Bearer"
          )
        """

        access_token: dict = cls._create_access_token(user)
        refresh_token: dict = cls._create_refresh_token(user)
        data: dict[str, str | datetime] = {
            "user_id": str(user.id),
            "refresh_token": refresh_token.get("token"),
            "expires_in": refresh_token.get("ex"),
        }
        await RefreshSessionRepo.add_one(session, **data)
        return TokenInfo(
            access_token=access_token.get("token"),
            refresh_token=refresh_token.get("token"),
        )

    @classmethod
    async def refresh_token(
        cls, session: AsyncSession, token: str
    ) -> TokenInfo:
        """
        Issue access token
        :return: TokenInfo(
            access_token: str,
            token_type: str = "Bearer"
          )
        """
        if refresh_session := await RefreshSessionRepo.get_one_or_none(
            session, refresh_token=token
        ):
            if datetime.now(UTC).timestamp() <= refresh_session.expires_in:
                if user := await UserRepo.get_one_or_none(
                    session, id=refresh_session.user_id
                ):
                    access_token: dict = cls._create_access_token(user)
                    return TokenInfo(access_token=access_token["token"])
        raise InvalidTokenException

    @classmethod
    async def logout(cls, session: AsyncSession, token: str) -> None:
        """
        Delete refresh token
        """
        if refresh_session := await RefreshSessionRepo.get_one_or_none(
            session,
            refresh_token=token,
        ):
            await RefreshSessionRepo.delete_one(session, refresh_session)

    @classmethod
    async def abort_all_sessions(
        self, session: AsyncSession, user_id: UUID
    ) -> None:
        """
        Delete all refresh tokens
        """
        if refresh_sessions := await RefreshSessionRepo.get(
            session, user_id=user_id
        ):
            await RefreshSessionRepo.delete_all(session, user_id=user_id)

    @classmethod
    def set_token_and_schema_in_cookies(
        cls,
        response: Response,
        key: str,
        token: str,
        scheme: str,
        max_age: int,
    ) -> None:
        response.set_cookie(key, token, max_age=max_age, httponly=True)
        response.set_cookie(
            "scheme",
            scheme,
            max_age=max_age,
            httponly=True,
        )

    @classmethod
    def _encode_jwt(
        cls,
        payload: dict,
        expire: int,
        private_key: str = Const.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.auth.algorithm,
    ) -> dict[str, str | int]:
        now: datetime = datetime.now(UTC)
        _expire_datetime: datetime = now + timedelta(minutes=expire)
        expire: int = int(round(_expire_datetime.timestamp()))
        to_encode: dict = payload.copy()
        to_encode.update(exp=expire, iat=now)
        jwt.api_jws.PyJWS.header_typ = False
        encoded: str = jwt.encode(
            payload=to_encode,
            key=private_key,
            algorithm=algorithm,
            headers={"Authorization": ""},
        )
        return {"token": encoded, "ex": expire}

    @classmethod
    def _create_token(
        cls, token_type: str, token_data: dict, expire: int
    ) -> dict[str, str | int]:
        if sub := token_data.get("sub"):
            if not isinstance(sub, str | None):
                token_data["sub"] = str(sub)

        payload: dict[str, str] = {settings.auth.token_type_field: token_type}
        payload.update(token_data)
        return cls._encode_jwt(payload=payload, expire=expire)

    @classmethod
    def _create_access_token(cls, user: UserSchema) -> dict[str, str | int]:
        token_data: dict[str, UUID | str] = {
            "sub": user.id,
            "email": user.email,
        }
        return cls._create_token(
            token_type=settings.auth.access_token_type,
            token_data=token_data,
            expire=settings.auth.access_token_expire_minutes,
        )

    @classmethod
    def _create_refresh_token(cls, user: UserSchema) -> dict[str, str | int]:
        token_data: dict[str, UUID] = {
            "sub": user.id,
        }
        return cls._create_token(
            token_type=settings.auth.refresh_token_type,
            token_data=token_data,
            expire=settings.auth.refresh_token_expire_minutes,
        )

    @classmethod
    def decode_jwt(
        cls,
        token: str | bytes,
        public_key: str = Const.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.auth.algorithm,
    ) -> dict:
        decoded: dict = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return decoded
