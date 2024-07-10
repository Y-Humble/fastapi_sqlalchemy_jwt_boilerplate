from datetime import UTC, datetime
from uuid import UUID as UUID_T
from sqlalchemy import ForeignKey, TIMESTAMP, VARCHAR, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base
from core.db.mixins import IdIntegerMixin


class RefreshSessionModel(IdIntegerMixin, Base):
    refresh_token: Mapped[str] = mapped_column(VARCHAR, index=True)
    expires_in: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(UTC),
        server_default=func.now(),
    )
    user_id: Mapped[UUID_T] = mapped_column(
        UUID, ForeignKey("users.id", ondelete="CASCADE")
    )
