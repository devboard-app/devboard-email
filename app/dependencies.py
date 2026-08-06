from app.config import settings
from fastapi import Header, HTTPException

async def verify_email_service_secret_key(x_service_key: str = Header(...)):
    if x_service_key != settings.EMAIL_SERVICE_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")