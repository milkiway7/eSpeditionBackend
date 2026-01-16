from fastapi import Request
from fastapi.responses import JSONResponse
from Helpers.logger import get_logger
from .domain_exceptions import (
    EntityNotFoundError,
    EntityAlreadyExistsError,
    ValidationError,
    UnauthorizedError,
    ForbiddenError,
    ExternalServiceUnavailable,
)
from .registration_exceptions import (
    KrsInactiveError,
    RegistrationNotFoundError,
    InvalidFinalTranzactionError,
)


def register_exception_handlers(app):
    @app.exception_handler(EntityNotFoundError)
    async def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
        get_logger().warning(f"Entity not found: {exc}")
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(EntityAlreadyExistsError)
    async def entity_already_exists_handler(
        request: Request, exc: EntityAlreadyExistsError
    ):
        get_logger().warning(f"Entity already exists: {exc}")
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        get_logger().warning(f"Validation error: {exc}")
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_error_handler(request: Request, exc: UnauthorizedError):
        get_logger().warning(f"Unauthorized: {exc}")
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(ForbiddenError)
    async def forbidden_error_handler(request: Request, exc: ForbiddenError):
        get_logger().warning(f"Forbidden: {exc}")
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(ExternalServiceUnavailable)
    async def external_service_unavailable_handler(
        request: Request, exc: ExternalServiceUnavailable
    ):
        get_logger().error(f"External service unavailable: {exc}")
        return JSONResponse(status_code=503, content={"detail": str(exc)})

    @app.exception_handler(KrsInactiveError)
    async def krs_inactive_error_handler(request: Request, exc: KrsInactiveError):
        get_logger().warning(f"KRS Inactive Error: {exc}")
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(RegistrationNotFoundError)
    async def registration_not_found_error_handler(
        request: Request, exc: RegistrationNotFoundError
    ):
        get_logger().warning(f"Registration not found: {exc}")
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    
    @app.exception_handler(InvalidFinalTranzactionError)
    async def invalid_final_tranzaction_error_handler(
        request: Request, exc: InvalidFinalTranzactionError
    ):
        get_logger().error(f"Invalid final transaction for registration: {exc}")
        return JSONResponse(status_code=500, content={"detail": str(exc)})
