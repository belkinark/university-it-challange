import logging

from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.dtos.task import (
    TaskUpdateDTO,
    TaskUpdateErrortDTO,
    TaskUpdateResultDTO,
)
from src.domain.entities.task import Task
from src.domain.enums.task_status import TaskStatus
from src.services.interfaces.repositories.task import ITaskRepository

logger = logging.getLogger(__name__)


class SQLAlchemyTaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def get_by_id(self, task_id: int) -> Task:
        query = select(Task).filter_by(id=task_id)
        result: Result = await self._session.execute(query)
        db_task = result.scalar_one_or_none()
        return Task.model_validate(db_task) if db_task else None

    async def start_processing(self, task: TaskUpdateDTO) -> Task:
        query = (
            update(Task)
            .where(Task.id == task.id)
            .values(status=TaskStatus.PROCESSING.value)
            .returning(Task)
        )
        result: Result = await self._session.execute(query)
        db_task = result.scalar_one_or_none()
        return Task.model_validate(db_task) if db_task else None

    async def update_result(self, task: TaskUpdateResultDTO) -> None:
        query = (
            update(Task)
            .where(Task.id == task.id)
            .values(
                status=TaskStatus.COMPLETED.value,
                result=task.result.model_dump()
            )
            .returning(Task.id)
        )
        await self._session.execute(query)

    async def update_error(self, task: TaskUpdateErrortDTO) -> None:
        query = (
            update(Task)
            .where(Task.id == task.id)
            .values(
                status=TaskStatus.FAILED.value,
                error=task.error
            )
            .returning(Task.id)
        )
        await self._session.execute(query)
