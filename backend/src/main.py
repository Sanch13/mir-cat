import asyncio
import logging

import uvicorn
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api.first import router as first_router
from src.apps.admin.make_admins import make_amis_admin, make_crud_admin, make_sql_admin
from src.config.server_settings import server_settings
from src.provides.adapters import ConfigProvider, SqlalchemyProvider


def container_factory() -> AsyncContainer:
    return make_async_container(
        SqlalchemyProvider(),
        ConfigProvider(),
    )


def init_di(app: FastAPI) -> None:
    container = container_factory()
    setup_dishka(container, app)


def init_routes(app: FastAPI) -> None:
    prefix: str = "/api/v1"
    app.include_router(
        router=first_router,
        prefix=f"{prefix}",
        tags=["First step"],
    )


def create_app() -> FastAPI:
    """Фабрика для создания FastAPI приложения"""
    app = FastAPI(
        title="Simple APP",
        description="Simple DDD example",
        version="1.0.0",
    )
    init_di(app)
    init_routes(app)  # Подключение роутеров

    make_sql_admin(app=app)
    make_amis_admin(app=app)
    make_crud_admin(app=app)

    return app


async def start_server(app: FastAPI) -> None:
    """Асинхронный запуск сервера"""
    config = uvicorn.Config(
        app=app,
        host=server_settings.HOST,
        port=server_settings.PORT,
        reload=server_settings.RELOAD,
        use_colors=server_settings.USE_COLORS,
        log_level=server_settings.LOG_LEVEL,
    )

    server = uvicorn.Server(config=config)
    logging.info(f"Starting server on {server_settings.HOST}:{server_settings.PORT}")

    await server.serve()


def main() -> None:
    """Основная функция запуска"""

    # Настройка логирования
    logging.basicConfig(
        level=getattr(logging, server_settings.LOG_LEVEL.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    application = create_app()

    try:
        asyncio.run(start_server(application))
    except (KeyboardInterrupt, SystemExit):
        logging.info("Server shutdown requested")
    except Exception as e:
        logging.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
