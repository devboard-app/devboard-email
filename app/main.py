from fastapi import Depends, FastAPI

from app.dependencies import verify_internal_api_key
from app.exception_handlers import register_exception_handlers
from app.routers import email

app = FastAPI(
    title="Devboard Email Service",
)
register_exception_handlers(app)
app.include_router(email.router, dependencies=[Depends(verify_internal_api_key)])

@app.get("/health")
async def health():
    return {"message":"ok"}