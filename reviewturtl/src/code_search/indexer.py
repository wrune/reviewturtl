from reviewturtl.src.code_search.preprocessor import TurtlPreprocessor
from qdrant_client import QdrantClient, models
from logging import getLogger
from typing import Optional, Any
from reviewturtl.src.data_models import IndexingMode
from reviewturtl.src.db_funcs.db_funcs import FileMetaDataManagement
import uuid

logger = getLogger(__name__)


class TurtlIndexer(TurtlPreprocessor):
    def __init__(
        self,
        qdrant_client: QdrantClient,
        fdm_management: FileMetaDataManagement,
        text_embedding_model=None,
        code_embedding_model=None,
        methods_dump_path: Optional[str] = None,
    ):
        super().__init__(methods_dump_path, text_embedding_model, code_embedding_model)
        self.qdrant_client = qdrant_client
        self.fdm_management = fdm_management

    def preprocess_methods_for_indexing(self, methods):
        """
        Preprocess the required methods for indexing
        Args:
            methods
        Returns:
        text_embeddings , code_embeddings
        """
        text_representations = self.preprocess_methods_for_text_embedding(methods)
        code_representations = self.preprocess_methods_for_code_embedding(methods)
        text_embeddings = self.get_text_embeddings(text_representations)
        code_embeddings = self.get_code_embeddings(code_representations)
        return text_embeddings, code_embeddings

    async def method_indexing_pipeline(self, methods, collection_name):
        """
        Method indexing pipeline that computes embeddings and uploads to Qdrant
        """
        # preprocess methods for indexing
        text_embeddings, code_embeddings = self.preprocess_methods_for_indexing(methods)
        # Check if collection exists
        if not self.qdrant_client.collection_exists(collection_name):
            try:
                # create the collection if it doesnot exist already
                self.qdrant_client.create_collection(
                    collection_name,
                    vectors_config={
                        "text": models.VectorParams(
                            size=text_embeddings.shape[1],
                            distance=models.Distance.COSINE,
                        ),
                        "code": models.VectorParams(
                            size=code_embeddings.shape[1],
                            distance=models.Distance.COSINE,
                        ),
                    },
                )
            except Exception as e:
                logger.error(
                    f"Error creating collection in qdrant for {collection_name} with error : {e}"
                )
                raise Exception(
                    f"Error creating collection in qdrant for {collection_name} with error : {e}"
                )

            try:
                # create a payload key for efficient filtering operations
                self.qdrant_client.create_payload_index(
                    collection_name=collection_name,
                    field_name="file_id",
                    field_schema="keyword",  # Create a keyword based schem on the file_id field
                )
            except Exception as e:
                logger.warning(
                    f"payload Creation for in qdrant for {collection_name} failed with error : {e}"
                )

        points = [
            models.PointStruct(
                id=str(uuid.uuid4()),  # generate a unique id for each point
                vector={
                    "text": text_embedding,
                    "code": code_embedding,
                },
                payload=structure,
            )
            for text_embedding, code_embedding, structure in zip(
                text_embeddings, code_embeddings, methods
            )
        ]
        try:
            # upload points to Qdrant
            self.qdrant_client.upload_points(
                collection_name, points=points, batch_size=64
            )
            # get the file_ids from the points
            file_ids = [point.payload["file_id"] for point in points]
            # set the is_indexed to true for the file_ids
            await self.fdm_management.set_is_indexed_true(file_ids)
            return True
        except Exception as e:
            logger.error(f"Error uploading points to Qdrant: {e}")
            return False

    async def index(
        self,
        collection_name: str,
        mode: Optional[str] = None,
        file_metadata: Optional[Any] = None,
    ):
        """
        Index documents in Qdrant for addition to the index
        Args:
            collection_name: str
            mode: str
            file_metadata: List[Dict[str, Any]]
        Returns:
            bool
        """
        if mode is None:
            # get methods from the specified path
            methods = self.get_methods(self.methods_dump_path)
        elif mode == IndexingMode.PARSE_FROM_FILE.value:
            file_metadata = [meta.model_dump() for meta in file_metadata]
            methods = self.get_methods_from_file_content(file_metadata)

        return await self.method_indexing_pipeline(methods, collection_name)

    async def update_index(
        self,
        collection_name: str,
        file_metadata: Optional[Any] = None,
    ):
        """
        Update the index for files that are edidted
        Args:
            collection_name: str
            file_metadata: List[Dict[str, Any]]
        Returns:
            bool
        """
        file_metadata = [meta.model_dump() for meta in file_metadata]
        file_ids = [meta["id"] for meta in file_metadata]
        # delete these points from qdrant
        try:
            # filter for file_id
            filter_for_file_ids = models.Filter(
                must=[
                    models.FieldCondition(
                        key="file_id",
                        match=models.MatchAny(any=file_ids),
                    )
                ]
            )
            logger.debug(f"Filter for file_ids: {filter_for_file_ids}")
            # delete with filter
            self.qdrant_client.delete(
                collection_name,
                points_selector=models.FilterSelector(filter=filter_for_file_ids),
            )
        except Exception as e:
            logger.error(f"Error deleting points from Qdrant: {e}")
            return False
        # set the is_indexed to false for the file_ids
        await self.fdm_management.set_is_indexed_false(file_ids)
        # get methods from the file content once the points are deleted
        methods = self.get_methods_from_file_content(file_metadata)
        return await self.method_indexing_pipeline(methods, collection_name)
