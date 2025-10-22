from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    email: str
    password: str


class TokenOutSchema(BaseModel):
    access_token: str
    expires_in: int
