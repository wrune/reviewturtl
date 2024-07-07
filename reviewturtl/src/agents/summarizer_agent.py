from reviewturtl.src.programmes.typed_cot import DspyProgramme
from reviewturtl.src.signatures.signatures import SummarizerSignature
from reviewturtl.src.agents.base_agent import Agent


class SummarizerAgent(Agent):
    def __init__(self):
        super().__init__(DspyProgramme(signature=SummarizerSignature))

    def forward(self, file_diff):
        self.prediction_object = self.programme.predictor(file_diff=file_diff)
        return self.prediction_object

    def walkthrough(self):
        return self.prediction_object.walkthrough

    def changes_in_tabular_description(self):
        return self.prediction_object.changes_in_tabular_description

    def __call__(self, file_diff):
        return self.forward(file_diff)


__all__ = ["SummarizerAgent"]
