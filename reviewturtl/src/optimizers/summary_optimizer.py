from reviewturtl.src.optimizers.mipro import MiproOptimizer
from reviewturtl.src.metrics.metrics import (
    SummarizerMetricwithgt,
    SummarizerEvaluatorWithoutGT,
)
from reviewturtl.src.signatures.signatures import SummarizerSignature
import os
import logging
from datetime import datetime

log = logging.getLogger(__name__)


class SummaryOptimizer:
    def __init__(
        self,
        csv_path,
        save_path=None,
        with_gt=True,
        save_extension=".json",
        optimizer_config=None,
    ):
        self.optimizer = MiproOptimizer()
        self.with_gt = with_gt
        self.trainset = self.optimizer.load_trainset(
            csv_path=csv_path,
            input_columns=["file_diff"],
            use_columns=None,
            output_columns=["changes_in_tabular_description", "walkthrough"],
        )
        self.optimizer_config = optimizer_config
        log.debug(f"Loaded trainset with {len(self.trainset)} examples")
        log.debug(f"Trainset: {self.trainset[0]}")
        filename = "summarizer_programme_" + str(datetime.now()) + save_extension
        if save_path is not None:
            self.save_path = os.path.join(save_path, filename)
        else:
            # save to relative path
            # get the parent directory of the current file
            self.save_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../programmes/compiled_programmes",
                filename,
            )

    def __call__(self):
        if self.with_gt:
            programme = self.optimizer.compile(
                self.trainset,
                SummarizerMetricwithgt,
                SummarizerSignature,
                optimizer_configs=self.optimizer_config,
            )
            programme.save(self.save_path)
            return programme
        else:
            programme = self.optimizer.compile(
                self.trainset,
                SummarizerEvaluatorWithoutGT,
                SummarizerSignature,
                optimizer_configs=self.optimizer_config,
            )
            programme.save(self.save_path)
            return programme
