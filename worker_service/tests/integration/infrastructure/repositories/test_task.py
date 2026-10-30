import pytest
import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.dtos.task import (
    TaskUpdateDTO,
    TaskUpdateErrortDTO,
    TaskUpdateResultDTO,
)
from src.domain.entities.task import Task, TaskResult
from src.domain.enums.task_status import TaskStatus
from src.infrastructure.repositories.task import SQLAlchemyTaskRepository


@pytest.fixture
def repo(db_session: AsyncSession) -> SQLAlchemyTaskRepository:
    return SQLAlchemyTaskRepository(session=db_session)


@pytest_asyncio.fixture
async def task_id(db_session: AsyncSession) -> int:
    result = await db_session.execute(
        insert(Task)
        .values(
            status=TaskStatus.PENDING.value,
            column="amount",
            data=b"amount\n10\n20\n",
        )
        .returning(Task.id)
    )
    return result.scalar_one()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_start_processing_updates_task_status(
    repo: SQLAlchemyTaskRepository,
    task_id: int,
) -> None:
    task = await repo.start_processing(TaskUpdateDTO(id=task_id))

    assert task is not None
    assert task.id == task_id
    assert task.status == TaskStatus.PROCESSING


@pytest.mark.integration
@pytest.mark.asyncio
async def test_start_processing_returns_none_for_missing_task(
    repo: SQLAlchemyTaskRepository,
) -> None:
    assert await repo.start_processing(TaskUpdateDTO(id=-1)) is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_result_marks_task_completed(
    repo: SQLAlchemyTaskRepository,
    task_id: int,
) -> None:
    result = TaskResult(count=2, min=10, max=20, mean=15)

    await repo.update_result(
        TaskUpdateResultDTO(id=task_id, result=result)
    )

    task = await repo.get_by_id(task_id)
    assert task is not None
    assert task.status == TaskStatus.COMPLETED
    assert task.result == result.model_dump()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_error_marks_task_failed(
    repo: SQLAlchemyTaskRepository,
    task_id: int,
) -> None:
    error = "column not found"

    await repo.update_error(TaskUpdateErrortDTO(id=task_id, error=error))

    task = await repo.get_by_id(task_id)
    assert task is not None
    assert task.status == TaskStatus.FAILED
    assert task.error == error
