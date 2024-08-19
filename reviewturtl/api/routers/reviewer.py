from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from reviewturtl.api.route_types import (
    ReviewerRequest,
    StandardResponse,
    ReviewerData,
)
from reviewturtl.src.agents.reviewer_agent import ReviewerAgent
from reviewturtl.logger import get_logger
from reviewturtl.settings import get_settings

log = get_logger(__name__)
router = APIRouter()
settings = get_settings()
reviewer = ReviewerAgent()


@router.post("/api/v1/review")
async def review_code_chunk(
    request: Request,
    body: ReviewerRequest,
) -> StandardResponse:
    try:
        file_diff_content = body.file_diff
        file_content = body.file_content
        prediction_object = reviewer(file_diff_content, file_content)
        log.debug(f"Review comments: {prediction_object.line_by_line_comments}")
        return StandardResponse(
            data=ReviewerData(
                line_by_line_comments=prediction_object.line_by_line_comments,
            )
        )
    except Exception as e:
        log.error(f"Error reviewing code chunk: {e}")
        return JSONResponse(
            status_code=400,
            content=StandardResponse(error=str(e)).model_dump(),
        )
