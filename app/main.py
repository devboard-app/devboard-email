from fastapi import FastAPI, Depends


app = FastAPI(
    title="Devboard Email Service",
)

@app.get("/health")
async def health():
    return {"message":"ok"}