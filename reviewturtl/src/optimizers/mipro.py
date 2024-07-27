from reviewturtl.src.optimizers.base_optimizer import TurtlBaseOptimizer
from reviewturtl.src.programmes.programmes import (
    TypedChainOfThoughtProgramme as DspyProgramme,
)
import dspy


class MiproOptimizer(TurtlBaseOptimizer):
    def __init__(self):
        super().__init__("MiPro")
        self.optimizer = None

    def initialize_optimizer(
        self,
        metric,
        number_of_candidates: int = 10,
        prompt_model=None,
        task_model=None,
    ):
        # Load the task and prompt models
        task_model = self.load_task_model(task_model)
        prompt_model = self.load_prompt_model(prompt_model)
        # Load the optimizer
        self.optimizer = self.load_optimizer(
            prompt_model, task_model, number_of_candidates, metric
        )

    def load_optimizer(self, prompt_model, task_model, number_of_candidates, metric):
        return dspy.teleprompt.MIPRO(
            prompt_model=prompt_model,
            task_model=task_model,
            num_candidates=number_of_candidates,
            metric=metric,
        )

    def compile(
        self,
        trainset,
        metric,
        signature,
        optimizer_configs: dict = None,
        eval_kwargs: dict = None,
    ):
        if optimizer_configs is None:
            optimizer_configs = {
                "num_trials": 3,
                "max_bootstrapped_demos": 10,
                "max_labeled_demos": 10,
            }
        if eval_kwargs is None:
            eval_kwargs = dict(num_threads=8, display_progress=True, display_table=0)

        optimizer = self.initialize_optimizer(metric)
        return optimizer.compile(
            DspyProgramme(signature),
            num_trials=optimizer_configs["num_trials"],
            max_bootstrapped_demos=optimizer_configs["max_bootstrapped_demos"],
            max_labeled_demos=optimizer_configs["max_labeled_demos"],
            trainset=trainset,
            eval_kwargs=eval_kwargs,
        )
