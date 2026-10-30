import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.task import Task
from src.domain.enums.task_status import TaskStatus
from src.infrastructure.repositories.task import SQLAlchemyTaskRepository


@pytest.fixture
def repo(db_session: AsyncSession) -> SQLAlchemyTaskRepository:
    return SQLAlchemyTaskRepository(session=db_session)


@pytest.fixture
def task() -> Task:
    return Task.create(
        status=TaskStatus.PENDING,
        column="amount",
        data=b"amount\n10\n20\n",
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_task_repository_create(
    repo: SQLAlchemyTaskRepository,
    task: Task,
) -> None:
    created_task = await repo.create(task)

    assert created_task.id is not None
    assert created_task.status == TaskStatus.PENDING
    assert created_task.column == "amount"
    assert created_task.data == task.data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_task_repository_get_all(
    repo: SQLAlchemyTaskRepository,
    task: Task,
) -> None:
    created_task = await repo.create(task)

    tasks = await repo.get_all()

    assert len(tasks) == 1
    assert tasks[0].id == created_task.id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_task_repository_get_by_id(
    repo: SQLAlchemyTaskRepository,
    task: Task,
) -> None:
    created_task = await repo.create(task)

    fetched_task = await repo.get_by_id(created_task.id)

    assert fetched_task is not None
    assert fetched_task.id == created_task.id
    assert fetched_task.column == task.column
    assert fetched_task.data == task.data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_task_repository_get_by_id_returns_none_for_missing_task(
    repo: SQLAlchemyTaskRepository,
) -> None:
    assert await repo.get_by_id(-1) is None
