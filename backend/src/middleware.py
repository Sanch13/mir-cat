import time

import structlog
from fastapi import Request
from opentelemetry import trace
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/metrics", "/health"]:
            return await call_next(request)

        # Получаем текущий Trace ID от OTel
        span = trace.get_current_span()
        trace_id = span.get_span_context().trace_id

        # Если трейсинг работает, trace_id будет числом. Превращаем в hex-строку.
        if trace_id == 0:
            trace_id_str = None
        else:
            trace_id_str = format(trace_id, "032x")

        # 1. Засекаем время и создаем context_id (request_id)
        start_time = time.perf_counter()

        # (Опционально) Если у тебя есть X-Request-ID хедер, можно взять его
        # request_id = request.headers.get("X-Request-ID")

        # 2. Очищаем контекст structlog для нового запроса
        # (Важно, чтобы данные старых запросов не прилипли к новому)
        structlog.contextvars.clear_contextvars()

        # 3. Привязываем базовую инфу
        structlog.contextvars.bind_contextvars(
            path=request.url.path,
            method=request.method,
            client_ip=request.client.host if request.client else "unknown",
            trace_id=trace_id_str,
        )
        logger.info("request_started")
        try:
            # === ВЫПОЛНЕНИЕ ЗАПРОСА ===
            response = await call_next(request)
            # ==========================

            process_time = time.perf_counter() - start_time

            # 4. Логируем успешный запрос
            logger.info(
                "request_finished",
                status_code=response.status_code,
                duration=round(process_time, 4),
            )
            return response

        except Exception as e:
            # 5. Логируем падение (500 error)
            process_time = time.perf_counter() - start_time
            logger.error(
                "request_failed",
                error=str(e),
                exc_info=True,
                duration=round(process_time, 4),
            )
            raise e
