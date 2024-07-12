from reviewturtl.src.programmes.typed_cot import DspyProgramme
from reviewturtl.src.signatures.signatures import ReviewerSignature
from reviewturtl.src.agents.base_agent import Agent


class ReviewerAgent(Agent):
    def __init__(self):
        super().__init__(DspyProgramme(signature=ReviewerSignature))

    def forward(self, file_diff):
        self.prediction_object = self.programme.predictor(file_diff=file_diff)
        return self.prediction_object
    
    def __call__(self, file_diff):
        return self.forward(file_diff)


__all__ = ["ReviewerAgent"]
