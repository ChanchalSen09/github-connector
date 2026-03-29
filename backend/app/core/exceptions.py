from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.models.responses import ErrorResponse


class AppError(Exception):
    def __init__(self, message: str, status_code: int, error_code: str) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class ConfigurationError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_code="config_error")


class AuthenticationError(AppError):
    def __init__(self, message: str = "GitHub authentication failed or the token lacks permission.") -> None:
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED, error_code="auth_error")


class NotFoundError(AppError):
    def __init__(self, message: str = "Requested GitHub resource was not found.") -> None:
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND, error_code="not_found")


class UpstreamValidationError(AppError):
    def __init__(self, message: str = "GitHub rejected the request payload.") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="upstream_validation_error",
        )


class UpstreamServiceError(AppError):
    def __init__(self, message: str = "GitHub service is temporarily unavailable.") -> None:
        super().__init__(message=message, status_code=status.HTTP_502_BAD_GATEWAY, error_code="upstream_error")


class UpstreamTimeoutError(AppError):
    def __init__(self, message: str = "GitHub request timed out.") -> None:
        super().__init__(message=message, status_code=status.HTTP_504_GATEWAY_TIMEOUT, error_code="upstream_timeout")


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=exc.error_code, message=exc.message).model_dump(),
    )


async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="validation_error",
            message="Request validation failed.",
            details=jsonable_encoder(exc.errors()),
        ).model_dump(),
    )


async def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="internal_server_error",
            message="An unexpected error occurred.",
            details={"exception_type": exc.__class__.__name__},
        ).model_dump(),
    )

