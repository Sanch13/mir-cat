from datetime import datetime
from uuid import UUID

from sqlalchemy import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

# class UUIDPkMixin:
#     id: Mapped[UUID] = mapped_column(
#         PostgreSQLUUID(as_uuid=True),
#         primary_key=True,
#         default=uuid4,
#         server_default=func.uuid_generate_v4(),
#     )


class UUIDPkMixin:
    id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True)


class DatetimeFieldsMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
