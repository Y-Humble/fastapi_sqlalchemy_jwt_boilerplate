from uuid import uuid4, UUID as UUID_T
from sqlalchemy import text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class IdIntegerMixin:
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)


class IdUUIDMixin:
    id: Mapped[UUID_T] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )
