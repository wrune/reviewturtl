from reviewturtl.src.code_search.preprocessor import TurtlPreprocessor
from logging import getLogger
from qdrant_client import QdrantClient
from qdrant_client.http.models import models
from typing import Dict, Any, Optional

logger = getLogger(__name__)


class TurtlSearch(TurtlPreprocessor):
    def __init__(
        self,
        qdrant_client: QdrantClient,
        methods_dump_path: Optional[str] = None,
        text_embedding_model=None,
        code_embedding_model=None,
        search_settings: Dict[str, Any] = None,
    ):
        super().__init__(methods_dump_path, text_embedding_model, code_embedding_model)
        self.qdrant_client = qdrant_client
        self.search_settings = search_settings

    def preprocess_for_search(self, query: str):
        text_embedding = self.get_text_embeddings(query)
        code_embedding = self.get_code_embeddings(query)
        return text_embedding, code_embedding

    def search(self, query: str, collection_name: str):
        text_embedding, code_embedding = self.preprocess_for_search(query)
        results = self.qdrant_client.query_points(
            collection_name,
            prefetch=[
                models.Prefetch(
                    query=list(text_embedding.flatten()),
                    using="text",
                    limit=self.search_settings["limit"],
                ),
                models.Prefetch(
                    query=list(code_embedding.flatten()),
                    using="code",
                    limit=self.search_settings["limit"],
                ),
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
        )
        return results
