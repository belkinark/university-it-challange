from fastapi import APIRouter

from src.api.system import router as system_router

router = APIRouter(prefix="/api")

router.include_router(system_router)
