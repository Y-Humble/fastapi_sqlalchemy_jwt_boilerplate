from httpx import AsyncClient, Cookies, Response

from apps.user.auth.messages import AuthResponseMessage


async def test_auth_cookies(async_client: AsyncClient) -> None:
    cookies: Cookies = async_client.cookies
    auth_cookies: list[str] = ["access_token", "refresh_token", "scheme"]
    for cookie in cookies:
        assert cookie in auth_cookies
        auth_cookies.remove(cookie)
    assert len(auth_cookies) == 0


async def test_refresh_token(async_client: AsyncClient) -> None:
    refresh: Response = await async_client.post("user/auth/refresh")
    assert refresh.status_code == 200


async def test_logout(async_client: AsyncClient) -> None:
    logout: Response = await async_client.delete("user/auth/logout")
    assert logout.status_code == 200
    assert logout.json() == AuthResponseMessage.LOGOUT
    assert not logout.cookies.__bool__()


async def test_abort_all_sessions(async_client: AsyncClient) -> None:
    abort: Response = await async_client.delete("user/auth/abort")
    assert abort.status_code == 200
    assert abort.json() == AuthResponseMessage.ABORT
    assert not abort.cookies.__bool__()
