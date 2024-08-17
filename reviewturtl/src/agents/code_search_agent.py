from reviewturtl.src.programmes.programmes import (
    TypedChainOfThoughtProgramme as DspyProgramme,
)
from reviewturtl.src.signatures.signatures import CodeSearchSignature
from reviewturtl.src.agents.base_agent import Agent
from reviewturtl.src.code_search.search import TurtlSearch
from reviewturtl.clients.qdrant_client import qdrant_client


class CodeSearchAgent(Agent):
    def __init__(self):
        self.class_name = __class__.__name__
        self.input_variables = ["search_query", "collection_name"]
        self.output_variables = ["code_search_results"]
        self.desc = """A code search agent that searches for code in a repository. \n
        It takes in a search query that will be used to fetch the results from a vector store and returns the top results from the vector store.\n
        It also takes in a collection name that will be used to fetch the results from a specific collection in the vector store.
        """
        super().__init__(DspyProgramme(signature=CodeSearchSignature))
        self.code_search = TurtlSearch(
            qdrant_client=qdrant_client, search_settings={"limit": 5}
        )

    def forward(self, search_query, collection_name, model=None):
        # Search for the code using hybrid search agent
        search_results = self.code_search.search(
            query=search_query, collection_name=collection_name
        )
        # For now pass the top result to the programme
        top_result = str(search_results.points[0].payload)
        # Pass the top result to the programme
        self.prediction_object = self.programme.forward(
            search_query=search_query,
            context_related_to_search_query=top_result,
            model=model,
        )
        return self.prediction_object

    def __call__(self, search_query, collection_name, model=None):
        return self.forward(search_query, collection_name, model=model)


__all__ = ["CodeSearchAgent"]
