from typing import Any
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from .base import AppException


async def app_exception_handler(request: Request, exc: Any) -> JSONResponse:  # AppException → Any
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def validation_exception_handler(request: Request, exc: Any) -> JSONResponse:  # RequestValidationError → Any
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "잘못된 요청입니다. 입력값을 확인해주세요."},
    )