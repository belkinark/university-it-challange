from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.repositories.messaging import TaskiqMessagingRepository
from src.infrastructure.repositories.task import SQLAlchemyTaskRepository
from src.services.interfaces.repositories.messaging import IMessagingRepository
from src.services.interfaces.repositories.task import ITaskRepository
from src.services.interfaces.uow import IUnitOfWork


class DatabaseUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        try:
            if exc_type is not None:
                await self.session.rollback()
            else:
                try:
                    await self.session.commit()
                except Exception:
                    await self.session.rollback()
                    raise
        finally:
            await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    @property
    def task_repository(self) -> ITaskRepository:
        return SQLAlchemyTaskRepository(self.session)

    @property
    def messaging_repository(self) -> IMessagingRepository:
        return TaskiqMessagingRepository()
