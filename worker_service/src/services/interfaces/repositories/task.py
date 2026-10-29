from abc import ABC, abstractmethod

from src.domain.dtos.task import (
    TaskUpdateDTO,
    TaskUpdateErrortDTO,
    TaskUpdateResultDTO,
)
from src.domain.entities.task import Task


class ITaskRepository(ABC):

    @abstractmethod
    async def get_by_id(self, task_id: int) -> Task:
        ...

    @abstractmethod
    async def start_processing(self, task: TaskUpdateDTO) -> Task:
        ...

    @abstractmethod
    async def update_result(self, task: TaskUpdateResultDTO) -> None:
        ...

    @abstractmethod
    async def update_error(self, task: TaskUpdateErrortDTO) -> None:
        ...
