from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.v1.schemas.errors import ErrorPayload, ErrorResponse
from src.domain import exceptions as domain_exc

EXC_MAP: dict[type[Exception], tuple[int, str]] = {
    domain_exc.Forbidden: (403, "FORBIDDEN"),
    ...: ...
}

def _make_handler(status_code: int, code: str):
    async def handler(_: Request, err: Exception):
        message = err.message if hasattr(err, 'message') else str(err)
        payload = ErrorPayload(code=code, message=message, details=None)
        return JSONResponse(
            status_code=status_code, content=ErrorResponse(error=payload).model_dump()
        )

    return handler

def init_exception_handlers(app: FastAPI) -> None:
    for exc_type, (status_code, code) in EXC_MAP.items():
        app.add_exception_handler(exc_type, _make_handler(status_code, code))
