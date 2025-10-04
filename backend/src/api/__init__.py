from fastapi import FastAPI

from src.api.first import router as first_router
from src.api.user.controllers import router as user_router


def init_routes(app: FastAPI) -> None:
    prefix: str = "/api/v1"
    app.include_router(router=first_router, prefix=f"{prefix}", tags=["First step"])
    app.include_router(router=user_router, prefix=f"{prefix}/user", tags=["Users"])
