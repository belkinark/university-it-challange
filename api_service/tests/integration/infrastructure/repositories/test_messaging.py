import pytest
from redis.asyncio import Redis

from src.core.config import settings
from src.infrastructure.repositories.messaging import TaskiqMessagingRepository


@pytest.fixture
def repo() -> TaskiqMessagingRepository:
    return TaskiqMessagingRepository()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_task_messaging_publishes_to_redis(
    repo: TaskiqMessagingRepository,
    redis_client: Redis,
) -> None:
    task_id = 12345

    await repo.create_task_messaging(task_id=task_id)

    messages = await redis_client.xrange(settings.services_queue.task_queue)
    assert len(messages) == 1
    payload = b" ".join(messages[0][1].values())
    assert str(task_id).encode() in payload
