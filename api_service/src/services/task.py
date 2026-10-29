import logging
from abc import ABC, abstractmethod

from src.domain.dtos.task import TaskCreateDTO
from src.domain.entities.task import Task
from src.services.interfaces.uow import IUnitOfWork

logger = logging.getLogger(__name__)


class ITaskService(ABC):

    @abstractmethod
    async def create(self, task_data: TaskCreateDTO) -> Task:
        ...

    @abstractmethod
    async def get_all(self) -> list[Task]:
        ...

    @abstractmethod
    async def get_by_id(self, task_id: int) -> Task:
        ...


class TaskService(ITaskService):
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def create(self, task_data: TaskCreateDTO) -> Task:
        async with self._uow as uow:
            task_data = Task.create(**task_data.model_dump())
            task = await uow.task_repository.create(task_data)
            messaging_repository = uow.messaging_repository

        await messaging_repository.create_task_messaging(task_id=task.id)
        return task

    async def get_all(self) -> list[Task]:
        async with self._uow as uow:
            return await uow.task_repository.get_all()

    async def get_by_id(self, task_id: int) -> list[Task]:
        async with self._uow as uow:
            return await uow.task_repository.get_by_id(
                task_id=task_id
            )
