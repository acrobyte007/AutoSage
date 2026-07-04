from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import time
from app.agent import get_research_answer,ResearchAgentResponse

from logger.logger import get_logger
logger = get_logger(__name__)

app = FastAPI()

class ResearchRequest(BaseModel):
    query: str = Field(..., description="The research topic or question")
    conversation: Optional[List[str]] = Field(
        default=None,
        description="Previous conversation history",
    )

class ResearchResponse(BaseModel):
    success: bool
    data: Optional[ResearchAgentResponse] = None
    error: Optional[str] = None
    processing_time: float


@app.get("/health")
async def health_check():
    return {
        "status": "ok"
    }


@app.post("/research", response_model=ResearchResponse)
async def research_endpoint(request: ResearchRequest):
    start_time = time.time()

    try:
        if not request.query.strip():
            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty",
            )

        logger.info(
            f"Processing research request: {request.query[:50]}"
        )

        result = await get_research_answer(
            query=request.query,
            conversation=request.conversation,
        )

        return ResearchResponse(
            success=True,
            data=result,
            processing_time=time.time() - start_time,
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Research request failed")

        return ResearchResponse(
            success=False,
            data=None,
            error=str(e),
            processing_time=time.time() - start_time,
        )
