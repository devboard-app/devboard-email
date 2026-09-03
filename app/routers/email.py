
from fastapi import APIRouter, status

from app.schemas.email import SendEmailRequest, SendEmailResponse
from app.services.email import send_email

router = APIRouter(prefix="/email", tags=["email"])

@router.post("/send", response_model= SendEmailResponse, status_code=status.HTTP_200_OK)
async def send(request:SendEmailRequest):
    await send_email(request.to, request.subject, request.template,  request.variables)
    return SendEmailResponse()
