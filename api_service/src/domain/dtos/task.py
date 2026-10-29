from pydantic import BaseModel

from src.domain.enums.task_status import TaskStatus


class TaskCreateDTO(BaseModel):
    status: TaskStatus = TaskStatus.PENDING
    column: str
    data: bytes
