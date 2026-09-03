from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.exceptions import (
    EmailDeliveryException,
    RecipientRefusedException,
    TemplateNotFoundException,
)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(TemplateNotFoundException)
    async def template_not_found_handler(request, exc):
        return JSONResponse(status_code=400, content={"detail": "Template not found"})

    @app.exception_handler(EmailDeliveryException)
    async def email_delivery_handler(request, exc):
        return JSONResponse(status_code=502, content={"detail": "Failed to deliver email"})

    @app.exception_handler(RecipientRefusedException)
    async def recipient_refused_handler(request, exc):
        return JSONResponse(status_code=400, content={"detail": "Recipient refused the email"})