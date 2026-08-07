from fastapi import Depends, FastAPI

from app.dependencies import verify_email_service_secret_key
from app.routers import email

app = FastAPI(
    title="Devboard Email Service",
)
app.include_router(email.router, dependencies=[Depends(verify_email_service_secret_key)])

@app.get("/health")
async def health():
    return {"message":"ok"}