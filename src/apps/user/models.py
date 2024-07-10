from enum import Enum
from sqlalchemy import Enum as pgEnum, LargeBinary, VARCHAR, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from core.db import Base
from core.db.mixins import IdUUIDMixin


class Status(Enum):
    ADMIN: str = "admin"
    ENJOYER: str = "enjoyer"
    BANNED: str = "banned"


class User(IdUUIDMixin, Base):
    username: Mapped[str] = mapped_column(VARCHAR(32), unique=True)
    email: Mapped[str] = mapped_column(VARCHAR, unique=True, index=True)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary)
    active: Mapped[bool] = mapped_column(
        Boolean, unique=False, default=True, server_default=expression.true()
    )
    status: Mapped[Status] = mapped_column(
        pgEnum(
            Status,
            name="status_enum",
            create_type=False,
            values_callable=lambda enum: [field.value for field in enum],
        ),
        default=Status.ENJOYER,
        server_default=Status.ENJOYER.value,
    )
