import base64
import time
from io import BytesIO
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

from app.agent import get_research_answer, ResearchAgentResponse
from logger.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/research",
    tags=["research"],
)


class ResearchRequest(BaseModel):
    query: str = Field(..., description="The research topic or question")
    conversation: Optional[List[str]] = Field(
        default=None,
        description="Optional conversation history",
    )


class ResearchResult(BaseModel):
    report: ResearchAgentResponse
    pdf: str


class ResearchResponse(BaseModel):
    success: bool
    data: Optional[ResearchResult] = None
    error: Optional[str] = None
    processing_time: float


def build_markdown_report(report: ResearchAgentResponse) -> str:
    """Convert the structured response into markdown."""

    markdown = f"""
# Summary

{report.summary}

# Key Points

{report.keypoints}

# Important Findings

{report.important_findings}

# Actionable Insights

{report.actionable_insights}

# References

"""

    for url in report.urls:
        markdown += f"- {url}\n"

    return markdown.strip()


def generate_pdf(report: ResearchAgentResponse) -> bytes:
    """
    Generate a PDF from ResearchAgentResponse.
    """

    markdown = build_markdown_report(report)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = []

    for line in markdown.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("# "):
            story.append(
                Paragraph(f"<b>{line[2:]}</b>", styles["Heading1"])
            )

        elif line.startswith("## "):
            story.append(
                Paragraph(f"<b>{line[3:]}</b>", styles["Heading2"])
            )

        elif line.startswith("- "):
            story.append(
                Paragraph(f"• {line[2:]}", styles["BodyText"])
            )

        else:
            story.append(
                Paragraph(line, styles["BodyText"])
            )

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf


@router.post("/", response_model=ResearchResponse)
async def research_endpoint(request: ResearchRequest):
    start_time = time.time()

    try:
        if not request.query.strip():
            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty",
            )

        logger.info(
            f"Processing research request: {request.query[:100]}"
        )

        result = await get_research_answer(
            query=request.query,
            conversation=request.conversation,
        )
        pdf_bytes = generate_pdf(result)
        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
        return ResearchResponse(
            success=True,
            data=ResearchResult(
                report=result,
                pdf=pdf_base64,
            ),
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