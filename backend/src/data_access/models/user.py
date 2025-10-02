from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.data_access.models import Base
from src.data_access.models.mixins import DatetimeFieldsMixin, UUIDPkMixin


class UserModel(Base, DatetimeFieldsMixin, UUIDPkMixin):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
