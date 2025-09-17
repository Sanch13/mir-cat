from fastapi import FastAPI

from src.api.first import router as first_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Simple APP",
        docs_url="/api/docs",
        description="Simple DDD example",
        debug=True,
    )
    app.include_router(first_router)
    return app
