from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from builders import FakeUser
from core.db import Base
from core.db.sidekick import db_sidekick
from core.setup import setup_app


@pytest.fixture(scope="session", autouse=True)
async def create_tables() -> AsyncGenerator[None, None]:
    async with db_sidekick._engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with db_sidekick._engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    test_app: FastAPI = setup_app()
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as async_client:
        yield async_client


@pytest.fixture(autouse=True)
async def register_and_login(async_client: AsyncClient):
    credentials = FakeUser().get_data()
    await async_client.post("/user/register", json=credentials)
    del credentials["email"]
    await async_client.post("user/auth/login", data=credentials)
