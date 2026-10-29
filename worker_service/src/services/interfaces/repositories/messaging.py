from abc import ABC, abstractmethod


class IMessagingRepository(ABC):

    @abstractmethod
    async def create_task_messaging(self, task_id: int) -> None:
        ...
