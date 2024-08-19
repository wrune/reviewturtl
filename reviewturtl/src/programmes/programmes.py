import dspy

class TypedChainOfThoughtProgramme(dspy.Module):
    def __init__(self, signature):
        super().__init__()
        self.predictor = dspy.TypedChainOfThought(signature)

    def forward(self, model=None, **kwargs):
        if model:
            with dspy.context(lm=model):
                return self.predictor(**kwargs)
        return self.predictor(**kwargs)

class TypedProgramme(dspy.Module):
    def __init__(self, signature):
        super().__init__()
        self.predictor = dspy.TypedPredictor(signature)

    def forward(self, model=None, **kwargs):
        if model:
            with dspy.context(lm=model):
                return self.predictor(**kwargs)
        return self.predictor(**kwargs)
