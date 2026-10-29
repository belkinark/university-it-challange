from fastapi import APIRouter, status

router = APIRouter(tags=["System"])

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
)
async def healthcheck():
    return {"status": "ok"}
