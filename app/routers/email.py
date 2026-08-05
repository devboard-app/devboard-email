
from fastapi import APIRouter, HTTPException, status
from app.schemas.email import SendEmailRequest, SendEmailResponse
from app.services.email import send_email

router = APIRouter(prefix="/email", tags=["email"])

@router.post("/send", response_model= SendEmailResponse, status_code=status.HTTP_200_OK)
async def send(request:SendEmailRequest):
    success = await send_email(request.to, request.subject, request.template,  request.variables)
    if not success:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send email")
    return SendEmailResponse()
