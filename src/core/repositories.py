from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepo[ModelT](ABC):
    """Abstract interface for interacting with repositories"""

    _model: ModelT

    @classmethod
    @abstractmethod
    async def get(
        cls, session: AsyncSession, offset: int, limit: int, **filter_by
    ) -> list[ModelT]:
        raise NotImplemented

    @classmethod
    @abstractmethod
    async def get_one_or_none(
        cls, session: AsyncSession, **filter_by
    ) -> ModelT | None:
        raise NotImplemented

    @classmethod
    @abstractmethod
    async def add(
        cls, session: AsyncSession, data: list[dict[str, Any]]
    ) -> list[ModelT]:
        raise NotImplemented

    @classmethod
    @abstractmethod
    async def add_one(cls, session: AsyncSession, **data) -> ModelT:
        raise NotImplemented

    @classmethod
    @abstractmethod
    async def update_one(
        cls, session: AsyncSession, obj: ModelT, **data
    ) -> ModelT:
        raise NotImplemented

    @classmethod
    @abstractmethod
    async def delete_one(cls, session: AsyncSession, obj: ModelT) -> None:
        raise NotImplemented

    @classmethod
    @abstractmethod
    async def delete_all(cls, session: AsyncSession, **filter_by) -> None:
        raise NotImplemented
