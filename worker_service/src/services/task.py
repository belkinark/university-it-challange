import csv
import io
import logging
from abc import ABC, abstractmethod

from src.domain.dtos.task import (
    TaskUpdateDTO,
    TaskUpdateErrortDTO,
    TaskUpdateResultDTO,
)
from src.domain.entities.task import TaskResult
from src.services.interfaces.uow import IUnitOfWork

logger = logging.getLogger(__name__)


class IProcessingService(ABC):

    @abstractmethod
    async def process_task(self, task_id: int) -> None:
        ...


class ProcessingService(IProcessingService):
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def process_task(self, task_id: int) -> None:
        async with self._uow as uow:
            try:
                task = await uow.task_repository.start_processing(
                    TaskUpdateDTO(id=task_id)
                )
                reader = csv.DictReader(io.StringIO(task.data.decode("utf-8")))
                data = [float(row[task.column]) for row in reader]
                len_data = len(data)

                result = TaskResult(
                    count=len_data,
                    min=min(data),
                    max=max(data),
                    mean=round(sum(data)/len_data, 1)
                )
                await uow.task_repository.update_result(
                    TaskUpdateResultDTO(id=task_id, result=result)
                )
            except Exception as e:
                await uow.task_repository.update_error(
                    TaskUpdateErrortDTO(id=task_id, error=str(e))
                )
                logger.exception(e)
