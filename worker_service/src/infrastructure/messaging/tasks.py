from dishka.integrations.taskiq import FromDishka, inject

from src.core.config import settings
from src.infrastructure.messaging.broker import broker
from src.services.task import IProcessingService


@broker.task(task_name=settings.services_queue.task_queue_name)
@inject(patch_module=True)
async def process_task(
    task_id: int,
    processing_service: FromDishka[IProcessingService],
) -> None:
    await processing_service.process_task(task_id)
