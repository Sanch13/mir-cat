from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str
    is_superuser: bool | None = None
    is_active: bool | None = None

class UserCreateSchema(UserUpdateSchema):
    password: str

class UserResponseSchema(UserUpdateSchema):
    email: str
    first_name: str
    last_name: str
    is_superuser: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime