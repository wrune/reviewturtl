from reviewturtl.src.code_search.preprocessor import TurtlPreprocessor
from qdrant_client import QdrantClient, models
import uuid
from logging import getLogger
from typing import Optional, Any
from reviewturtl.src.data_models import IndexingMode

logger = getLogger(__name__)


class TurtlIndexer(TurtlPreprocessor):
    def __init__(
        self,
        qdrant_client: QdrantClient,
        text_embedding_model=None,
        code_embedding_model=None,
        methods_dump_path: Optional[str] = None,
    ):
        super().__init__(methods_dump_path, text_embedding_model, code_embedding_model)
        self.qdrant_client = qdrant_client
        self.db_functions = None

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

    def method_indexing_pipeline(self, methods, collection_name):
        """
        Method indexing pipeline that computes embeddings and uploads to Qdrant
        """
        # preprocess methods for indexing
        text_embeddings, code_embeddings = self.preprocess_methods_for_indexing(methods)
        # Check if collection exists
        if not self.qdrant_client.collection_exists(collection_name):
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
        points = [
            models.PointStruct(
                id=uuid.uuid4().hex,
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
            return True
        except Exception as e:
            logger.error(f"Error uploading points to Qdrant: {e}")
            return False

    def index(
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

        return self.method_indexing_pipeline(methods, collection_name)

    def update_index(self, collection_name: str, file_metadata: Optional[Any] = None):
        """
        Update the index for files that are edidted
        Args:
            collection_name: str
            file_metadata: List[Dict[str, Any]]
        Returns:
            bool
        """
        file_metadata = [meta.model_dump() for meta in file_metadata]
        # get the id's of the files from primary database
        file_ids = self.db_functions.get_file_ids(file_metadata)
        # delete these points from qdrant
        try:
            self.qdrant_client.delete_points(
                collection_name, points_selector=models.PointIdsList(points=file_ids)
            )
        except Exception as e:
            logger.error(f"Error deleting points from Qdrant: {e}")
            return False
        # get methods from the file content once the points are deleted
        methods = self.get_methods_from_file_content(file_metadata)
        return self.method_indexing_pipeline(methods, collection_name)
