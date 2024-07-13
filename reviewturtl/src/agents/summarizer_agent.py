from reviewturtl.src.programmes.programmes import TypedChainOfThoughtProgramme as DspyProgramme
from reviewturtl.src.signatures.signatures import SummarizerSignature
from reviewturtl.src.agents.base_agent import Agent


class SummarizerAgent(Agent):
    def __init__(self):
        super().__init__(DspyProgramme(signature=SummarizerSignature))

    def forward(self, file_diff,model=None):
        self.prediction_object = self.programme.forward(file_diff=file_diff,model=model)
        return self.prediction_object

    def walkthrough(self):
        return self.prediction_object.walkthrough

    def changes_in_tabular_description(self):
        return self.prediction_object.changes_in_tabular_description

    def __call__(self, file_diff,model=None):
        return self.forward(file_diff,model=model)


__all__ = ["SummarizerAgent"]
