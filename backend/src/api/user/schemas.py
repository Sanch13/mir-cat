from datetime import datetime

from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str
    password: str


class UserResponseSchema(BaseModel):
    first_name: str | None
    last_name: str | None
    email: str
    created_at: datetime
    updated_at: datetime
    is_superuser: bool
    is_active: bool


class UserAuthSchema(BaseModel):
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    pass
