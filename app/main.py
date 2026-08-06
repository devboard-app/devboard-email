from fastapi import FastAPI, Depends
from app.routers import email
from app.dependencies import verify_email_service_secret_key
app = FastAPI(
    title="Devboard Email Service",
    dependencies=[Depends(verify_email_service_secret_key)]
)
app.include_router(email.router)

@app.get("/health")
async def health():
    return {"message":"ok"}