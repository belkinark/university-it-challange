from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

from src.domain.exceptions import (
    Forbidden,
)


def create_exception_handler(
        status_code: int,
        detail: str
    ) -> Callable[[Request, Any], Coroutine[Any, Any, Response]]:
    """
    Фабрика для создания исключений
    :param status_code: код статуса
    :param detail: текст ошибки
    :return: HTTPException
    """
    async def handler(request: Request, exc: Exception) -> Response:
        return JSONResponse(status_code=status_code, content={"detail": detail})

    return handler

exception_handlers: dict[
    type[Exception],
    Callable[[Request, Any],Coroutine[Any, Any, Response]]
] = {
    Forbidden: create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Недостаточно прав для выполнения операции."
    ),
}
