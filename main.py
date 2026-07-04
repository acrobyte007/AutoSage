from fastapi import FastAPI
from app.router import router
from logger.logger import get_logger
logger = get_logger(__name__)

app = FastAPI()



@app.get("/health")
async def health_check():
    return {
        "status": "ok"
    }

app.include_router(router)