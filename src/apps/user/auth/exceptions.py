from fastapi import status

from core.exceptions import HTTPExceptionBase


class AuthErrorMessages:
    __slots__ = ()
    COOKIES_NOT_FOUND_400: str = "Expected cookies not found"
    INVALID_TOKEN_401: str = "Invalid token"
    UNAUTHORIZED_USER_401: str = "Not authenticated"
    INVALID_TOKEN_TYPE_401: str = "Invalid token type '{}' expected '{}'"
    EXPIRED_TOKEN_401: str = "Token has expired"


class InvalidTokenException(HTTPExceptionBase):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = AuthErrorMessages.INVALID_TOKEN_401


class UnauthorizedUserException(HTTPExceptionBase):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = AuthErrorMessages.UNAUTHORIZED_USER_401


class InvalidTokenTypeException(HTTPExceptionBase):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, token_type, expected_type):
        self.detail = AuthErrorMessages.INVALID_TOKEN_TYPE_401.format(
            token_type, expected_type
        )
