from reviewturtl.src.code_search.preprocessor import TurtlPreprocessor
from qdrant_client import QdrantClient, models
import uuid
from logging import getLogger

logger = getLogger(__name__)


class TurtlIndexer(TurtlPreprocessor):
    def __init__(
        self,
        methods_dump_path: str,
        qdrant_client: QdrantClient,
        text_embedding_model=None,
        code_embedding_model=None,
    ):
        super().__init__(methods_dump_path, text_embedding_model, code_embedding_model)
        self.qdrant_client = qdrant_client

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

    def index(self, collection_name: str):
        """
        Index documents in Qdrant
        """
        # get methods from the specified path
        methods = self.get_methods(self.methods_dump_path)
        # preprocess methods for indexing
        text_embeddings, code_embeddings = self.preprocess_methods_for_indexing(methods)
        # Check if collection exists
        if not self.qdrant_client.collection_exists(collection_name):
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
