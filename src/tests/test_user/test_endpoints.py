from datetime import datetime

from httpx import AsyncClient, Response

from apps.user.messages import UserResponseMessage
from tests.builders import FakeUser
from apps.user import Status


async def test_register_user(async_client: AsyncClient) -> None:
    list_credentials = [FakeUser().get_data() for _ in range(10)]
    for credentials in list_credentials:
        register: Response = await async_client.post(
            "/user/register", json=credentials
        )
        assert register.status_code == 201
        user: dict = register.json()
        assert user["username"] == credentials["username"]
        assert user["email"] == credentials["email"]
        assert user["active"]
        assert user["status"] == Status.ENJOYER.value


async def test_get_current_user(async_client: AsyncClient) -> None:
    current_user: Response = await async_client.get("/user/me")
    assert current_user.status_code == 200
    user: dict = current_user.json()
    assert user["login_at"] == datetime.now().strftime("%d %B %Y")


async def test_update_user(async_client: AsyncClient) -> None:
    list_new_data = [FakeUser().get_data() for _ in range(10)]
    for new_data in list_new_data:
        current_user: Response = await async_client.put(
            "/user/me", json=new_data
        )
        assert current_user.status_code == 200
        user: dict = current_user.json()
        assert user["username"] == new_data["username"]
        assert user["email"] == new_data["email"]


async def test_delete_current_user(async_client: AsyncClient) -> None:
    current_user: Response = await async_client.delete("/user/me")
    assert current_user.status_code == 200
    assert current_user.json() == UserResponseMessage.INACTIVE_STATUS
