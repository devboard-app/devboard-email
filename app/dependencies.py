import hmac

from fastapi import Header, HTTPException

from app.config import settings


async def verify_internal_api_key(x_service_key: str = Header(...)):
    if hmac.compare_digest(x_service_key, settings.INTERNAL_API_KEY):
        raise HTTPException(status_code=403, detail="Forbidden")