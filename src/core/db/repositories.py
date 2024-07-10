from typing import Any

from sqlalchemy import Insert, insert, Select, select, Delete, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories import AbstractRepo
from core.db.base import Base


type ModelT[T: Base] = Base


class SQlAlchemyRepo[ModelT](AbstractRepo):
    """
    An interface for interacting with SQL repositories
    methods:
        get, get_one_or_none, add, add_one, update_one, delete_one, delete_all
    """

    _model: ModelT

    @classmethod
    async def get(
        cls,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        **filter_by,
    ) -> list[ModelT]:
        stmt: Select = (
            select(cls._model)
            .filter_by(**filter_by)
            .offset(offset)
            .limit(limit)
        )
        result: Result = await session.execute(stmt)
        rows: ModelT = result.scalars().all()
        return list(rows)

    @classmethod
    async def get_one_or_none(
        cls, session: AsyncSession, **filter_by
    ) -> ModelT | None:
        stmt: Select = select(cls._model).filter_by(**filter_by)
        result: Result = await session.execute(stmt)
        row: ModelT = result.scalars().one_or_none()
        return row

    @classmethod
    async def add(
        cls, session: AsyncSession, data: list[dict[str, Any]]
    ) -> list[ModelT]:
        stmt: Insert = insert(cls._model).values(data).returning(cls._model)
        result: Result = await session.execute(stmt)
        await session.commit()
        rows: ModelT = result.scalars().all()
        return list(rows)

    @classmethod
    async def add_one(cls, session: AsyncSession, **data) -> list[ModelT]:
        stmt: ModelT = cls._model(**data)
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
        return stmt

    @classmethod
    async def update_one(
        cls, session: AsyncSession, obj: ModelT, **data
    ) -> ModelT:
        for name, value in data.items():
            setattr(obj, name, value)
        await session.commit()
        return obj

    @classmethod
    async def delete_one(cls, session: AsyncSession, obj: ModelT) -> None:
        await session.delete(obj)
        await session.commit()

    @classmethod
    async def delete_all(cls, session: AsyncSession, **filter_by) -> None:
        stmt: Delete = delete(cls._model).filter_by(**filter_by)
        await session.execute(stmt)
        await session.commit()
