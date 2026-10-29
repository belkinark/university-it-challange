from fastapi import APIRouter

from src.api.v1.endpoints.tasks import router as tasks_router

router = APIRouter(prefix="/v1")

router.include_router(tasks_router)
