from fastapi import FastAPI
from app.api.analyze import router as analyze_router

app = FastAPI(title="Creator Intelligence Platform")

app.include_router(analyze_router)


@app.get("/")
async def root():
    return {
        "message": "Creator Intelligence Platform Running"
    }