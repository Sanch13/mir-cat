import asyncio
import logging

import uvicorn
from fastapi import FastAPI

from backend.src.api.first import router as first_router
from backend.src.config.server_settings import server_settings


def create_app() -> FastAPI:
    """Фабрика для создания FastAPI приложения"""
    app = FastAPI(
        title="Simple APP",
        description="Simple DDD example",
        version="1.0.0",
    )
    # Подключение роутеров
    app.include_router(first_router)
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
