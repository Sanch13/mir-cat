import taskiq_fastapi
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

from src.config.settings import settings

result_backend = RedisAsyncResultBackend(
    redis_url=settings.redis.redis_url,
)

broker = RedisStreamBroker(
    url=settings.redis.redis_url,
).with_result_backend(result_backend)

scheduler = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])

taskiq_fastapi.init(broker, "src.main:create_app")
