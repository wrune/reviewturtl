from typing import List
import uuid
from reviewturtl.logger import get_logger

log = get_logger(__name__)


class FileMetaDataManagement:
    def __init__(self, db_client):
        self.db_client = db_client

    async def get_file_metadata(self, file_id):
        return await self.db_client.file_metadata.find_unique(where={"id": file_id})

    # Function to get file IDs based on file paths and repo ID
    async def get_file_ids_by_paths_and_repo(self, file_paths: List[str], repo_id: str):
        file_metadata = await self.db_client.file_metadata.find_many(
            where={"file_path": {"in": file_paths}, "repo_id": repo_id}
        )
        return [metadata.id for metadata in file_metadata]

    # Function to set is_indexed to true by accepting the id field of file_metadata
    async def set_is_indexed_true(self, file_ids: List[str]):
        return await self.db_client.file_metadata.update_many(
            where={"id": {"in": file_ids}}, data={"is_indexed": True}
        )

    # Function to set is_indexed to false by accepting the id field of file_metadata
    async def set_is_indexed_false(self, file_ids: List[str]):
        return await self.db_client.file_metadata.update_many(
            where={"id": {"in": file_ids}}, data={"is_indexed": False}
        )

    # Function to add multiple entries to the file_metadata table
    async def add_file_metadata(self, repo_id: str, file_paths: List[str]):
        data = [
            {"id": str(uuid.uuid4()), "repo_id": repo_id, "file_path": file_path}
            for file_path in file_paths
        ]
        status = await self.db_client.file_metadata.create_many(data=data)
        if status:
            return [d["id"] for d in data]
        else:
            log.error("Failed to add file metadata")
            raise Exception("Failed to add file metadata")
