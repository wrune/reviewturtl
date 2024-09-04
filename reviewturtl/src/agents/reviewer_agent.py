from reviewturtl.src.programmes.programmes import (
    TypedChainOfThoughtProgramme as DspyProgramme,
)
from reviewturtl.src.signatures.signatures import ReviewerSignature
from reviewturtl.src.agents.base_agent import Agent


class ReviewerAgent(Agent):
    def __init__(self):
        super().__init__(DspyProgramme(signature=ReviewerSignature))

    def forward(self, file_diff, file_content, request_id: str = None, model=None):
        self.prediction_object = self.programme.forward(
            file_diff=file_diff,
            file_content=file_content,
            request_id=request_id,
            model=model,
        )
        return self.prediction_object

    def __call__(self, file_diff, file_content, request_id: str = None, model=None):
        return self.forward(file_diff, file_content, request_id=request_id, model=model)


__all__ = ["ReviewerAgent"]
