import json
from typing import List, Dict, Any, Optional
from reviewturtl.src.code_search.utils import (
    convert_chunk_to_text,
    extract_nodes_from_files,
)
from fastembed import TextEmbedding
from sentence_transformers import SentenceTransformer
import numpy as np
from reviewturtl.src.data_models import ExtractedNode


class TurtlPreprocessor:
    def __init__(
        self,
        methods_dump_path: Optional[str],
        text_embedding_model=None,
        code_embedding_model=None,
    ):
        """
        Initializes the indexer
        Args:
            methods_dump_path (str): Path to the dump file
            text_embedding_model (str): Embedding model to use for text
            code_embedding_model (str): Embedding model to use for code
        """
        self.methods_dump_path = methods_dump_path
        if text_embedding_model is None:
            # Default embedding model
            self.text_embedding_model = TextEmbedding(
                "sentence-transformers/all-MiniLM-L6-v2"
            )
        else:
            # Custom embedding model
            self.text_embedding_model = TextEmbedding(text_embedding_model)
        if code_embedding_model is None:
            # Default embedding model
            self.code_embedding_model = SentenceTransformer(
                "jinaai/jina-embeddings-v2-base-code", trust_remote_code=True
            )
        else:
            # Custom embedding model
            self.code_embedding_model = TextEmbedding(code_embedding_model)

    @staticmethod
    def get_methods(methods_dump_path: str):
        """
        Loads the methods from the dump file
        Returns:
            List[Dict[str, Any]]: List of methods
        """
        with open(methods_dump_path) as f:
            return json.load(f)

    def get_methods_from_file_content(
        self, file_contents: List[Dict[str, str]]
    ) -> List[ExtractedNode]:
        """
        Loads the methods from the file content
        Returns:
            List[Dict[str, Any]]: List of methods
        """
        return extract_nodes_from_files(file_contents)

    @staticmethod
    def preprocess_methods_for_text_embedding(methods: List[Dict[str, Any]]):
        """
        Converts the methods to text representations
        Returns:
            List[str]: List of text representations
        """
        text_representations = list(map(convert_chunk_to_text, methods))
        return text_representations

    @staticmethod
    def preprocess_methods_for_code_embedding(methods: List[Dict[str, Any]]):
        """
        Converts the methods to code representations
        Returns:
            List[str]: List of code representations
        """
        code_snippets = [structure["context"]["snippet"] for structure in methods]
        return code_snippets

    def get_text_embeddings(self, text_representations: List[str]):
        """
        Gets the text embeddings for the text representations
        Returns:
            List[List[float]]: List of text embeddings
        """
        return np.array(list(self.text_embedding_model.embed(text_representations)))

    def get_code_embeddings(self, code_representations: List[str]):
        """
        Gets the code embeddings for the code representations
        Returns:
            List[List[float]]: List of code embeddings
        """
        return np.array(list(self.code_embedding_model.encode(code_representations)))
