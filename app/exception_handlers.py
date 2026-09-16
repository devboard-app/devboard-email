from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import (
    EmailDeliveryException,
    RecipientRefusedException,
    TemplateNotFoundException,
)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(TemplateNotFoundException)
    async def template_not_found_handler(request, exc):
        return JSONResponse(status_code=400, content={"detail": "Template not found", "errors": None})

    @app.exception_handler(EmailDeliveryException)
    async def email_delivery_handler(request, exc):
        return JSONResponse(status_code=502, content={"detail": "Failed to deliver email", "errors": None})

    @app.exception_handler(RecipientRefusedException)
    async def recipient_refused_handler(request, exc):
        return JSONResponse(status_code=400, content={"detail": "Recipient refused the email", "errors": None})

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request, exc):
        errors: dict[str, list[str]] = {}
        for error in exc.errors():
            field = str(error["loc"][-1]) if error["loc"] else "non_field_errors"
            errors.setdefault(field, []).append(error["msg"])
        return JSONResponse(status_code=422, content={"detail": next(iter(errors.values()))[0], "errors": errors})

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail, "errors": None})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request, exc):
        return JSONResponse(status_code=500, content={"detail": "Unexpected error occurred", "errors": None})