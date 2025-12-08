import functools
import inspect

from opentelemetry import trace

# Создаем трейсер. Имя "app.manual" будет видно в свойствах спана,
# чтобы отличать автоматические спаны от твоих ручных.
tracer = trace.get_tracer("app.manual_instrumentation")


def traced(name: str | None = None):
    """
    Декоратор для создания ручного спана (Span) в OpenTelemetry.

    :param name: Название спана в Grafana.
                             Если не передано, используется имя функции.
    """

    def decorator(func):
        # Логика для асинхронных функций (async def)
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                span_name = name or func.__name__
                with tracer.start_as_current_span(span_name):
                    return await func(*args, **kwargs)

            return async_wrapper

        # Логика для синхронных функций (def)
        else:

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                span_name = name or func.__name__
                with tracer.start_as_current_span(span_name):
                    return func(*args, **kwargs)

            return sync_wrapper

    return decorator
