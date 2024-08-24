from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from reviewturtl.logger import get_logger
from reviewturtl.settings import get_settings
from reviewturtl.api.route_types import (
    StandardResponse,
    IndexCodeRequest,
    IndexCodeResponse,
)

from reviewturtl.src.code_search.indexer import TurtlIndexer
from qdrant_client import QdrantClient


router = APIRouter()
settings = get_settings()

qdrant_client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)

indexer = TurtlIndexer(qdrant_client=qdrant_client)
log = get_logger(__name__)


@router.post("/api/v1/index_code")
async def index_code(
    request: Request,
    body: IndexCodeRequest,
) -> StandardResponse:
    try:
        collection_name = body.collection_name
        mode = body.mode
        file_metadata = body.file_metadata

        # Log the original query
        log.info(f"Indexing code with mode: {mode}")
        log.info(f"File metadata: {file_metadata}")
        # Call the code search agent with conversation history
        result = indexer.index(
            collection_name=collection_name,
            mode=mode,
            file_metadata=file_metadata,
        )
        log.info(f"Indexing code with mode: {mode}")
        log.info(f"File metadata: {file_metadata}")
        return StandardResponse(data=IndexCodeResponse(success=result))
    except Exception as e:
        log.error(f"Error in code search: {e}", exc_info=True)
        return JSONResponse(
            status_code=400,
            content=StandardResponse(error=str(e)).model_dump(),
        )
