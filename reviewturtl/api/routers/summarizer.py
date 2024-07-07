from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from reviewturtl.api.route_types import (
    SummarizerRequest,
    SummarizerResponse,
    SummarizerData,
)
from reviewturtl.src.agents.summarizer_agent import SummarizerAgent
from reviewturtl.logger import get_logger
from reviewturtl.settings import get_settings

log = get_logger(__name__)
router = APIRouter()
settings = get_settings()
summarizer = SummarizerAgent()


@router.post("/api/v1/summarize")
async def summarize_code_chunk(
    request: Request,
    body: SummarizerRequest,
) -> SummarizerResponse:
    try:
        file_diff_content = body.file_diff
        summary = summarizer(file_diff_content)
        reasoning = summarizer.reason()
        log.debug(f"Summarized code chunk: {summary}")
        return SummarizerResponse(
            data=SummarizerData(
                walkthrough=summary.walkthrough,
                tabular_summary=summary.changes_in_tabular_description,
                reason=reasoning,
            )
        )
    except Exception as e:
        log.error(f"Error summarizing code chunk: {e}")
        return JSONResponse(
            status_code=400,
            content=SummarizerResponse(error=str(e)).model_dump(),
        )
