import asyncio
from contextlib import asynccontextmanager

import structlog
import uvicorn
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.taskiq import setup_dishka as setup_dishka_taskiq
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_fastapi_instrumentator import Instrumentator

from src.application.admin import init_sql_admin
from src.config import all_settings as settings
from src.config import broker
from src.logging_setup import setup_logging
from src.middleware import RequestLogMiddleware
from src.presentation.api import init_routes
from src.presentation.api.exception_handler import init_exception_handlers
from src.provides import container_factory

# import sentry_sdk
#
# sentry_sdk.init(
#     dsn=settings.sentry.dsn,
#     send_default_pii=True,
#     traces_sample_rate=1.0,
#     profiles_sample_rate=1.0,
# )

setup_logging()
logger = structlog.get_logger()


# === НАСТРОЙКА TRACING (OpenTelemetry) ===
def setup_tracing():
    # 1. Настраиваем "Ресурс" (имя сервиса, которое будет в Grafana)
    resource = Resource.create(
        attributes={"service.name": "fastapi_app", "service.version": "1.0.0"}
    )

    # 2. Создаем провайдер трейсов
    tracer_provider = TracerProvider(resource=resource)

    # 3. Настраиваем экспортер (куда слать данные) -> В Tempo
    # 'tempo' - это имя контейнера из docker-compose
    otlp_exporter = OTLPSpanExporter(endpoint="tempo:4317", insecure=True)

    # 4. Добавляем процессор (он шлет данные пачками, чтобы не тормозить)
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)

    # 5. Устанавливаем глобальный провайдер
    trace.set_tracer_provider(tracer_provider)


def init_di(app: FastAPI) -> None:
    container = container_factory()
    setup_dishka_fastapi(container=container, app=app)
    setup_dishka_taskiq(container=container, broker=broker)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup", status="started")
    if not broker.is_worker_process:
        await broker.startup()
    yield
    if not broker.is_worker_process:
        await broker.shutdown()
    logger.info("shutdown", status="stopped")


def create_app() -> FastAPI:
    """Фабрика для создания FastAPI приложения"""
    setup_tracing()

    app = FastAPI(
        lifespan=lifespan,
        title="Simple APP",
        description="Simple DDD example",
        version="1.0.0",
    )
    init_di(app)
    init_exception_handlers(app)
    init_routes(app)  # Подключение роутеров
    init_sql_admin(app=app)

    app.add_middleware(RequestLogMiddleware)

    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=[".*admin.*", "/metrics"],
        env_var_name="ENABLE_METRICS",
        inprogress_name="inprogress",
        inprogress_labels=True,
    )
    instrumentator.instrument(app).expose(app)

    FastAPIInstrumentor.instrument_app(app, excluded_urls="metrics,/metrics,health,/health")
    return app


async def start_server(app: FastAPI) -> None:
    """Асинхронный запуск сервера"""
    config = uvicorn.Config(
        app=app,
        host=settings.server.HOST,
        port=settings.server.PORT,
        reload=settings.server.RELOAD,
        use_colors=settings.server.USE_COLORS,
        log_level=settings.server.LOG_LEVEL,
    )

    server = uvicorn.Server(config=config)
    logger.info(f"Starting server on {settings.server.HOST}:{settings.server.PORT}")

    await server.serve()


def main() -> None:
    """Основная функция запуска"""

    # Настройка логирования
    # logging.basicConfig(
    #     level=getattr(logging, settings.server.LOG_LEVEL.upper()),
    #     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # )

    application = create_app()

    try:
        asyncio.run(start_server(application))
    except (KeyboardInterrupt, SystemExit):
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
