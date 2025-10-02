from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserInputDto:
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    is_superuser: bool = False
    is_active: bool = True


# ToDo: понять используется ли пароль в ДТО.
@dataclass
class UserOutputDto:
    id: UUID
    email: str
    password: str
    created_at: datetime | None
    updated_at: datetime | None
    first_name: str | None = None
    last_name: str | None = None
    is_superuser: bool = False
    is_active: bool = True
