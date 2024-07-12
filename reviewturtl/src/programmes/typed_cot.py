import dspy
class DspyProgramme(dspy.Module):
    def __init__(self, signature):
        super().__init__()
        self.predictor = dspy.TypedChainOfThought(signature)

    def forward(self, context):
        return dspy.Prediction(answer=self.predictor(context=context))
