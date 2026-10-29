from taskiq.kicker import AsyncKicker

from src.core.config import settings
from src.infrastructure.messaging.broker import broker
from src.services.interfaces.repositories.messaging import IMessagingRepository


class TaskiqMessagingRepository(IMessagingRepository):
    def __init__(self) -> None:
        self._kicker = AsyncKicker(
            task_name=settings.services_queue.task_queue_name,
            broker=broker,
            labels={},
        )

    async def create_task_messaging(self, task_id: int) -> None:
        await self._kicker.kiq(task_id=task_id)
