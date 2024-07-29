from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from reviewturtl.logger import get_logger
from reviewturtl.settings import get_settings
from reviewturtl.api.route_types import (
    StandardResponse,
    CodeSearchRequest,
    CodeSearchResponse,
)
from reviewturtl.src.code_search.search import TurtlSearch
from reviewturtl.clients.qdrant_client import qdrant_client
from reviewturtl.src.agents.code_search_agent import CodeSearchAgent

log = get_logger(__name__)
router = APIRouter()
settings = get_settings()

search = TurtlSearch(qdrant_client=qdrant_client, search_settings={"limit": 5})
code_search_agent = CodeSearchAgent()


@router.post("/api/v1/code_search")
async def code_search(
    request: Request,
    body: CodeSearchRequest,
) -> StandardResponse:
    try:
        search_query = body.search_query
        collection_name = body.collection_name
        search_results = search.search(
            query=search_query, collection_name=collection_name
        )
        top_result = str(search_results.points[0].payload)
        llm_response = code_search_agent(
            search_query=search_query, context_related_to_search_query=top_result
        ).response_for_search_query
        log.debug(f"Search results: {search_results}")
        return StandardResponse(
            data=CodeSearchResponse(response_for_search_query=llm_response)
        )
    except Exception as e:
        log.error(f"Error summarizing code chunk: {e}")
        return JSONResponse(
            status_code=400,
            content=StandardResponse(error=str(e)).model_dump(),
        )
