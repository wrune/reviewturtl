from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from reviewturtl.logger import get_logger
from reviewturtl.settings import get_settings, get_4o_token_model
from reviewturtl.api.route_types import (
    StandardResponse,
    CodeSearchRequest,
    CodeSearchResponse,
)

from reviewturtl.src.agents.code_search_agent import CodeSearchAgent

code_search_agent = CodeSearchAgent()
log = get_logger(__name__)
router = APIRouter()
settings = get_settings()


@router.post("/api/v1/code_search")
async def code_search(
    request: Request,
    body: CodeSearchRequest,
) -> StandardResponse:
    try:
        search_query = body.search_query
        collection_name = body.collection_name
        conversation_history = str(body.conversation_history)

        # get a better token model
        model = get_4o_token_model()

        # Log the original query
        log.info(f"Original search query: {search_query}")

        # Call the code search agent with conversation history
        result = code_search_agent(
            search_query=search_query,
            collection_name=collection_name,
            conversation_history=conversation_history,
            model=model,
        )
        llm_response = result.response_for_search_query
        return StandardResponse(
            data=CodeSearchResponse(response_for_search_query=llm_response)
        )
    except Exception as e:
        log.error(f"Error in code search: {e}")
        return JSONResponse(
            status_code=400,
            content=StandardResponse(error=str(e)).model_dump(),
        )
