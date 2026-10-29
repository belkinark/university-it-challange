from pydantic import BaseModel

from src.domain.entities.task import TaskResult
from src.domain.enums.task_status import TaskStatus


class TaskResponse(BaseModel):
    id: int
    status: TaskStatus
    column: str
    result: TaskResult | None = None
    error: str | None = None
