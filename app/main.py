from fastapi import FastAPI, Depends
from app.routers import email

app = FastAPI(
    title="Devboard Email Service",
)
app.include_router(email.router)

@app.get("/health")
async def health():
    return {"message":"ok"}