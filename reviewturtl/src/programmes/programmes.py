import dspy
from reviewturtl.src.signatures.signatures import QueryRewriterSignature

class TypedChainOfThoughtProgramme(dspy.Module):
    def __init__(self, signature):
        super().__init__()
        self.predictor = dspy.TypedChainOfThought(signature)

    def forward(self, model=None, **kwargs):
        if model:
            with dspy.context(lm=model):
                return self.predictor(**kwargs)
        return self.predictor(**kwargs)

class QueryRewriterProgramme(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.TypedPredictor(QueryRewriterSignature)

    def forward(self, model=None, **kwargs):
        if model:
            with dspy.context(lm=model):
                return self.predictor(**kwargs)
        return self.predictor(**kwargs)
