from abc import ABC, abstractmethod

from src.domain.entities.task import Task


class ITaskRepository(ABC):

    @abstractmethod
    async def create(self, task_data: Task) -> Task:
        ...

    @abstractmethod
    async def get_all(self) -> list[Task]:
        ...

    @abstractmethod
    async def get_by_id(self, task_id: int) -> Task:
        ...
