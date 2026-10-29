from pydantic import BaseModel, ConfigDict, Field

from src.domain.entities.mixins import DateTimeMixin
from src.domain.enums.task_status import TaskStatus


class TaskResult(BaseModel):
    count: int
    min: float
    max: float
    mean: float


class Task(DateTimeMixin):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    status: TaskStatus
    column: str
    data: bytes = Field(exclude=True, repr=False)
    result: TaskResult | None = None
    error: str | None = None

    @classmethod
    def create(
        cls,
        status: TaskStatus,
        column: str,
        data: bytes,
        result: TaskResult | None = None,
        error: str | None = None,
    ) -> "Task":
        return cls(
            status=status,
            column=column,
            data=data,
            result=result,
            error=error,
        )
