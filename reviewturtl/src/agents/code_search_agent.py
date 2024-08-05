from reviewturtl.src.programmes.programmes import (
    TypedChainOfThoughtProgramme as DspyProgramme,
)
from reviewturtl.src.signatures.signatures import CodeSearchSignature
from reviewturtl.src.agents.base_agent import Agent


class CodeSearchAgent(Agent):
    def __init__(self):
        self.class_name = __class__.__name__
        self.input_variables = ["search_query", "context_related_to_search_query"]
        self.output_variables = ["code_search_results"]
        self.desc = "A code search agent that searches for code in a repository."
        super().__init__(DspyProgramme(signature=CodeSearchSignature))

    def forward(self, search_query, context_related_to_search_query, model=None):
        self.prediction_object = self.programme.forward(
            search_query=search_query,
            context_related_to_search_query=context_related_to_search_query,
            model=model,
        )
        return self.prediction_object

    def __call__(self, search_query, context_related_to_search_query, model=None):
        return self.forward(search_query, context_related_to_search_query, model=model)


__all__ = ["CodeSearchAgent"]
