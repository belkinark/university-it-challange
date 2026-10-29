import logging
from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, File, Form, UploadFile, status

from src.api.v1.schemas.tasks import TaskResponse
from src.domain.dtos.task import TaskCreateDTO
from src.services.task import ITaskService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    route_class=DishkaRoute
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[TaskResponse],
)
async def get_tasks(
    task_service: FromDishka[ITaskService],
) -> list[dict]:
    tasks = await task_service.get_all()
    return [TaskResponse(**task.model_dump()) for task in tasks]


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskResponse,
)
async def get_task(
    task_id: int,
    task_service: FromDishka[ITaskService],
) -> list[dict]:
    task = await task_service.get_by_id(task_id=task_id)
    return TaskResponse(**task.model_dump())


@router.post(
    "/",
    summary="Создание и отправка задачи в очередь задач.",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    column: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
    task_service: FromDishka[ITaskService],
) -> list[dict]:
    created_task = await task_service.create(
        TaskCreateDTO(
            column=column,
            data=await file.read()
        )
    )
    return TaskResponse(**created_task.model_dump())
