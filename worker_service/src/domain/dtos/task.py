from pydantic import BaseModel

from src.domain.entities.task import TaskResult


class TaskUpdateDTO(BaseModel):
    id: int


class TaskUpdateResultDTO(TaskUpdateDTO):
    result: TaskResult


class TaskUpdateErrortDTO(TaskUpdateDTO):
    error: str
