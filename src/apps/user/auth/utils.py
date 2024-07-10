from fastapi import Request
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows

from apps.user.auth.exceptions import UnauthorizedUserException


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        token_type: str,
        scheme_name: str | None = None,
        scopes: dict[str, str] | None = None,
        auto_error: bool = True,
    ) -> None:
        scopes: dict[str, str] = scopes if scopes else {}
        password: dict[str, str | dict[str, str]] = {
            "tokenUrl": tokenUrl,
            "scopes": scopes,
        }
        flows: OAuthFlows = OAuthFlows(password=password)
        self.token_type: str = token_type
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> str | None:
        scheme, param = get_authorization_scheme_param_from_cookie(
            request,
            self.auto_error,
            self.token_type,
        )
        return param


def get_authorization_scheme_param_from_cookie(
    request: Request,
    auto_error,
    token_type: str,
) -> tuple[str, str] | None | UnauthorizedUserException:
    scheme: str = request.cookies.get("scheme")
    param: str = request.cookies.get(token_type)
    if not param or scheme.lower() != "bearer":
        if auto_error:
            raise UnauthorizedUserException
        return None
    return scheme, param
