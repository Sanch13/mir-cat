import asyncio
import logging

import uvicorn
from fastapi import FastAPI

from src.api.first import router as first_router


class ServerConfig:
    """Конфигурация сервера"""

    HOST = "0.0.0.0"
    PORT = 8000
    RELOAD = True  # False для программного запуска
    LOG_LEVEL = "info"  # info для production, debug для разработки
    USE_COLORS = True


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
        host=ServerConfig.HOST,
        port=ServerConfig.PORT,
        reload=ServerConfig.RELOAD,
        use_colors=ServerConfig.USE_COLORS,
        log_level=ServerConfig.LOG_LEVEL,
    )

    server = uvicorn.Server(config=config)
    logging.info(f"Starting server on {ServerConfig.HOST}:{ServerConfig.PORT}")

    await server.serve()


def main() -> None:
    """Основная функция запуска"""

    # Настройка логирования
    logging.basicConfig(
        level=getattr(logging, ServerConfig.LOG_LEVEL.upper()),
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
