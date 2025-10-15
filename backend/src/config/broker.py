import taskiq_fastapi
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

from src.config.redis_settings import redis_config

result_backend = RedisAsyncResultBackend(
    redis_url=redis_config.redis_url,
)

broker = RedisStreamBroker(
    url=redis_config.redis_url,
).with_result_backend(result_backend)

scheduler = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])

taskiq_fastapi.init(broker, "src.main:create_app")
