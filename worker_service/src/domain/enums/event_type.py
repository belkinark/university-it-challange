from enum import Enum

from src.core.config import settings


class EventType(str, Enum):
    TASKS = settings.services_queue.task_queue
