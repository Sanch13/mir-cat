from fastapi import FastAPI

from src.presentation.api.auth.routes import router as auth_router
from src.presentation.api.first import router as first_router
from src.presentation.api.user.routes import router as user_router


def init_routes(app: FastAPI) -> None:
    prefix: str = "/presentation/v1"
    app.include_router(router=auth_router, prefix=f"{prefix}/auth", tags=["Auth"])
    app.include_router(router=user_router, prefix=f"{prefix}/users", tags=["Users"])
    app.include_router(router=first_router, prefix=f"{prefix}", tags=["First step"])
