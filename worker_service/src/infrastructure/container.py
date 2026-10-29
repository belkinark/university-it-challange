from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db import postgres
from src.infrastructure.uow import DatabaseUnitOfWork
from src.services.interfaces.uow import IUnitOfWork
from src.services.task import IProcessingService, ProcessingService


class Container(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_session(self) -> AsyncIterable[AsyncSession]:
        if postgres.session_maker is None:
            raise RuntimeError("Session maker is not initialized")
        async with postgres.session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def provide_uow(self, session: AsyncSession) -> IUnitOfWork:
        return DatabaseUnitOfWork(session)

    @provide(scope=Scope.REQUEST)
    async def provide_processing_service(self, uow: IUnitOfWork) -> IProcessingService:
        return ProcessingService(uow)
