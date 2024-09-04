from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from reviewturtl.logger import get_logger
from reviewturtl.settings import get_settings
from reviewturtl.api.route_types import (
    StandardResponse,
    IndexCodeRequest,
    IndexCodeResponse,
    FileAction,
)

from reviewturtl.src.code_search.indexer import TurtlIndexer
from qdrant_client import QdrantClient
from reviewturtl.src.db_funcs.db_funcs import FileMetaDataManagement
from reviewturtl.clients.db_client import get_prisma_client
import asyncio

router = APIRouter()
settings = get_settings()

qdrant_client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)

log = get_logger(__name__)

initialization_complete = asyncio.Event()


async def initialize_components():
    global prisma_client, fdm_management, indexer
    try:
        prisma_client = await get_prisma_client()
        fdm_management = FileMetaDataManagement(prisma_client)
        indexer = TurtlIndexer(
            qdrant_client=qdrant_client, fdm_management=fdm_management
        )
        log.info("Components initialized successfully")
    except Exception as e:
        log.error(f"Error initializing components: {e}", exc_info=True)
        raise
    finally:
        initialization_complete.set()  # Signal that initialization is complete


# Check if the event loop is running and handle initialization accordingly
loop = asyncio.get_event_loop()
if loop.is_running():
    # If the event loop is already running, use create_task
    loop.create_task(initialize_components())
else:
    # If no event loop is running, use asyncio.run
    asyncio.run(initialize_components())


@router.post("/api/v1/index_code")
async def index_code(
    request: Request,
    body: IndexCodeRequest,
) -> StandardResponse:
    try:
        # Ensure initialization is complete before proceeding
        await initialization_complete.wait()
        request_id = request.headers.get("X-Request-ID")
        collection_name = body.collection_name
        mode = body.mode
        file_metadata = body.file_metadata
        log.debug(f"File metadata: {file_metadata}")
        # get the repo_id from the request_body
        repo_id = body.repo_id
        # get all the files where the action is ADD
        files_to_index = [
            file for file in file_metadata if file.action == FileAction.ADD
        ]
        log.debug(f"Files to index: {files_to_index}")
        # get all the file where the action is Modify
        files_to_modify = [
            file for file in file_metadata if file.action == FileAction.MODIFY
        ]
        log.debug(f"Files to modify: {files_to_modify}")
        # Index the Files that needs to be added
        result_add_files = False
        if files_to_index:
            # Add these entries in the database
            file_ids_to_be_indexed = await fdm_management.add_file_metadata(
                repo_id=repo_id, file_paths=[file.file_path for file in files_to_index]
            )
            # add these file_ids to the file_metadata for the files to be indexed
            for file, file_id in zip(files_to_index, file_ids_to_be_indexed):
                file.id = file_id
            try:
                result_add_files = await indexer.index(
                    collection_name=collection_name,
                    mode=mode,
                    file_metadata=files_to_index,
                )
            except Exception as e:
                log.error(f"Error in indexing files: {e}", exc_info=True)
        # Update the files that are modified
        result_update_files = False
        if files_to_modify:
            # get the id's of the files from primary database
            file_ids_to_modify = await fdm_management.get_file_ids_by_paths_and_repo(
                file_paths=[file.file_path for file in files_to_modify], repo_id=repo_id
            )
            # add the file_ids to the file_metadata for the files to be modified
            for file, file_id in zip(files_to_modify, file_ids_to_modify):
                file.id = file_id
            try:
                result_update_files = await indexer.update_index(
                    collection_name=collection_name,
                    file_metadata=files_to_modify,
                )
            except Exception as e:
                log.error(f"Error in updating files: {e}", exc_info=True)
        return StandardResponse(
            data=IndexCodeResponse(
                success=(
                    (result_add_files if files_to_index else True)
                    and (result_update_files if files_to_modify else True)
                )
            )
        )
    except Exception as e:
        log.error(f"Error in code search: {e}", request_id=request_id, exc_info=True)
        return JSONResponse(
            status_code=400,
            content=StandardResponse(error=str(e)).model_dump(),
        )
