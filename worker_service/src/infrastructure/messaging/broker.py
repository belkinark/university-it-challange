from taskiq_redis import RedisStreamBroker

from src.core.config import settings

broker = RedisStreamBroker(
    url=settings.redis.url,
    queue_name=settings.services_queue.task_queue,
    consumer_group_name="task-workers",
    xread_count=1,
)
