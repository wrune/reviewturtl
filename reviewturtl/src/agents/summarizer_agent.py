from reviewturtl.src.programmes.typed_cot import DspyProgramme
from reviewturtl.src.signatures.signatures import SummarizerSignature
from reviewturtl.src.agents.base_agent import Agent


class SummarizerAgent(Agent):
    def __init__(self):
        super().__init__(DspyProgramme(signature=SummarizerSignature))

    def summarize(self, old_chunk_code, new_chunk_code):
        self.prediction_object = self.programme.predictor(
            old_chunk_code=old_chunk_code, new_chunk_code=new_chunk_code
        )
        return self.prediction_object.summary

    def __call__(self, old_chunk_code, new_chunk_code):
        return self.summarize(old_chunk_code, new_chunk_code)


__all__ = ["SummarizerAgent"]
