import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api import init_routes
from src.apps.admin import init_sql_admin
from src.config.server_settings import server_settings
from src.core.bg_tasks.redis_broker import broker
from src.provides import container_factory


def init_di(app: FastAPI) -> None:
    container = container_factory()
    setup_dishka(container, app)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        await broker.startup()
    yield
    if not broker.is_worker_process:
        await broker.shutdown()


def create_app() -> FastAPI:
    """Фабрика для создания FastAPI приложения"""
    app = FastAPI(
        lifespan=lifespan,
        title="Simple APP",
        description="Simple DDD example",
        version="1.0.0",
    )
    init_di(app)
    init_routes(app)  # Подключение роутеров
    init_sql_admin(app=app)
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
