import dspy
from reviewturtl.api.cache_tools import cache
from reviewturtl.logger import get_logger

log = get_logger(__name__)


def add_tokens_to_cache(request_id: str, prediction_tokens: int):
    token_till_now = cache.get(request_id)
    cache.set(request_id, token_till_now + prediction_tokens)


class TypedChainOfThoughtProgramme(dspy.Module):
    def __init__(self, signature):
        super().__init__()
        self.predictor = dspy.TypedChainOfThought(signature)

    def forward(self, model=None, request_id: str = None, **kwargs):
        if model:
            with dspy.context(lm=model):
                prediction = self.predictor(**kwargs)
                try:
                    prediction_tokens = model.history[-1]["response"]["usage"][
                        "total_tokens"
                    ]
                    add_tokens_to_cache(request_id, prediction_tokens)
                except Exception as e:
                    log.error(f"Error adding tokens to cache: {e}", exc_info=True)
            return prediction
        else:
            prediction = self.predictor(**kwargs)
            model = dspy.settings.lm

            try:
                prediction_tokens = model.history[-1]["response"]["usage"][
                    "total_tokens"
                ]
                add_tokens_to_cache(request_id, prediction_tokens)
            except Exception as e:
                log.error(f"Error adding tokens to cache: {e}", exc_info=True)
            return prediction


class TypedProgramme(dspy.Module):
    def __init__(self, signature):
        super().__init__()
        self.predictor = dspy.TypedPredictor(signature)

    def forward(self, model=None, request_id: str = None, **kwargs):
        if model:
            with dspy.context(lm=model):
                prediction = self.predictor(**kwargs)
                try:
                    prediction_tokens = model.history[-1]["response"]["usage"][
                        "total_tokens"
                    ]
                    add_tokens_to_cache(request_id, prediction_tokens)
                except Exception as e:
                    log.error(f"Error adding tokens to cache: {e}", exc_info=True)
                return prediction
        else:
            prediction = self.predictor(**kwargs)
            model = dspy.settings.lm
            try:
                prediction_tokens = model.history[-1]["response"]["usage"][
                    "total_tokens"
                ]
                add_tokens_to_cache(request_id, prediction_tokens)
            except Exception as e:
                log.error(f"Error adding tokens to cache: {e}", exc_info=True)
            return prediction
