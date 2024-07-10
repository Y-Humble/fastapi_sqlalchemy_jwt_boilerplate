from typing import AsyncGenerator

from sqlalchemy import Pool, URL
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker as asm,
    AsyncSession,
    AsyncEngine,
)

from core.config import settings


class DBSidekick:
    """
    Connecting to database, create session, dispose connection pool,
    create and drop all databases for testing
    """

    def __init__(
        self,
        url: URL | str,
        echo: bool,
        echo_pool: bool,
        engine_options: dict[str, int | Pool],
    ) -> None:
        self._engine: AsyncEngine = create_async_engine(
            url=url, echo=echo, echo_pool=echo_pool, **engine_options
        )
        self.session_factory: asm[AsyncSession] = asm(
            bind=self._engine,
            future=True,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """Uses for dependecy injection"""
        async with self.session_factory() as session:
            yield session

    async def dispose(self) -> None:
        """Dispose of the connection pool"""
        await self._engine.dispose()


db_sidekick: DBSidekick = DBSidekick(
    url=settings.db.url,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    engine_options=settings.db.engine_options,
)
