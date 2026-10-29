from redis.asyncio import Redis

from src.domain.enums.event_type import EventType
from src.services.interfaces.repositories.messaging import IMessagingRepository


class RedisMessagingRepository(IMessagingRepository):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def create_task_messaging(self, task_id: int) -> None:
        await self._redis.xadd(
            EventType.TASKS,
            {"task_id": str(task_id)},
        )
