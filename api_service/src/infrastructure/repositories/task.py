import logging

from sqlalchemy import Result, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.task import Task
from src.services.interfaces.repositories.task import ITaskRepository

logger = logging.getLogger(__name__)


class SQLAlchemyTaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, task_data: Task) -> Task:
        insert_data = task_data.model_dump(exclude_none=True)
        insert_data["data"] = task_data.data
        query = insert(Task).values(insert_data).returning(Task)
        result: Result = await self._session.execute(query)
        db_task = result.unique().scalar_one()
        return Task.model_validate(db_task)

    async def get_all(self) -> list[Task]:
        query = select(Task)
        result: Result = await self._session.execute(query)
        db_tasks = result.unique().scalars().all()
        return [Task.model_validate(task) for task in db_tasks]

    async def get_by_id(self, task_id: int) -> Task:
        query = select(Task).filter_by(id=task_id)
        result: Result = await self._session.execute(query)
        db_task = result.scalar_one_or_none()
        return Task.model_validate(db_task) if db_task else None
