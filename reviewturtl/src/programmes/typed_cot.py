import dspy
from reviewturtl.settings import get_settings

cfg = get_settings()
api_key = cfg.OPENAI_API_KEY
turbo = dspy.OpenAI(
    model="gpt-4o",
    api_key=api_key,
    max_tokens=3000,
)
dspy.settings.configure(lm=turbo)


class DspyProgramme(dspy.Module):
    def __init__(self, signature):
        super().__init__()
        self.predictor = dspy.TypedChainOfThought(signature)

    def forward(self, context):
        return dspy.Prediction(answer=self.predictor(context=context))
