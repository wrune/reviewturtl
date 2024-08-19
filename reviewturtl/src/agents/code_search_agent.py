from reviewturtl.src.programmes.programmes import (
    TypedChainOfThoughtProgramme as DspyProgramme,
)
from reviewturtl.src.signatures.signatures import CodeSearchSignature, QueryRewriterSignature
from reviewturtl.src.agents.base_agent import Agent
from reviewturtl.src.code_search.search import TurtlSearch
from reviewturtl.clients.qdrant_client import qdrant_client
import dspy
from typing import List, Dict
import logging


class CodeSearchAgent(Agent):
    def __init__(self):
        self.class_name = __class__.__name__
        self.input_variables = ["search_query", "collection_name", "conversation_history"]
        self.output_variables = ["code_search_results"]
        self.desc = """A code search agent that searches for code in a repository. \n
        It takes in a search query that will be used to fetch the results from a vector store and returns the top results from the vector store.\n
        It also takes in a collection name that will be used to fetch the results from a specific collection in the vector store.
        The agent uses query rewriting based on conversation history to improve search results.
        """
        super().__init__(DspyProgramme(signature=CodeSearchSignature))
        self.code_search = TurtlSearch(
            qdrant_client=qdrant_client, search_settings={"limit": 5}
        )
        self.logger = logging.getLogger(self.class_name)

    def forward(self, search_query: str, collection_name: str, conversation_history: List[Dict[str, str]], model=None):
        # Rewrite the query based on conversation history
        rewritten_query = self.rewrite_query(search_query, conversation_history)

        # Search for the code using hybrid search agent with the rewritten query
        search_results = self.code_search.search(
            query=rewritten_query, collection_name=collection_name
        )
        # For now pass the top result to the programme
        top_result = str(search_results.points[0].payload)
        # Pass the top result to the programme
        self.prediction_object = self.programme.forward(
            search_query=rewritten_query,
            context_related_to_search_query=top_result,
            model=model,
        )
        return self.prediction_object

    def __call__(self, search_query, collection_name, model=None):
        return self.forward(search_query, collection_name, model=model)


    def rewrite_query(self, query: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Rewrites the query based on conversation history using TypedPredictor.

        Args:
            query (str): The original search query.
            conversation_history (List[Dict[str, str]]): A list of dictionaries containing the conversation history.

        Returns:
            str: The rewritten query.
        """
        self.logger.info(f"Original query: {query}")
        rewritten_query = self.query_rewriter(
            conversation_history=conversation_history,
            query=query
        )
        self.logger.info(f"Rewritten query: {rewritten_query.rewritten_query}")
        return rewritten_query.rewritten_query



__all__ = ["CodeSearchAgent"]
