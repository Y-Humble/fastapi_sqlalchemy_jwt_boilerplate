from fastapi import Depends
from jwt.exceptions import InvalidTokenError

from core.config import settings
from apps.user.auth.exceptions import InvalidTokenException
from apps.user.auth.services import AuthService
from apps.user.auth.utils import OAuth2PasswordBearerWithCookie as CookieOAuth2

oauth2_access_scheme: CookieOAuth2 = CookieOAuth2(
    tokenUrl=settings.auth.token_url,
    token_type=settings.auth.access_token_type,
)
oauth2_refresh_scheme: CookieOAuth2 = CookieOAuth2(
    tokenUrl=settings.auth.token_url,
    token_type=settings.auth.refresh_token_type,
)


def get_current_token_payload(token: str) -> dict[str, str]:
    try:
        payload: dict = AuthService.decode_jwt(token=token)
    except InvalidTokenError:
        raise InvalidTokenException
    return payload


def get_access_token_payload(
    token: str = Depends(oauth2_access_scheme),
) -> dict[str, str]:
    return get_current_token_payload(token)


def get_refresh_token_payload(
    token: str = Depends(oauth2_refresh_scheme),
) -> dict[str, str]:
    return get_current_token_payload(token)
