import dspy
from reviewturtl.src.signatures.signatures import (
    SummarizerEvaluatorWithGT,
    SummarizerEvaluatorWithoutGT,
)


def SummarizerMetricwithoutgt(gold, pred, trace=None):
    """
    Wrapper for the SummarizerEvaluator
    """
    alignment_criterion = "Rate the **walkthrough** and **changes in tabular description** on a Scale of 1 to 5"
    evaluator = dspy.TypedPredictor(SummarizerEvaluatorWithoutGT)(
        # criterion is the alignment criterion
        criterion=alignment_criterion,
        # file_diff is the file diff given to the system
        file_diff=gold.file_diff,
        # walkthrough is the walkthrough given to the system
        walkthrough=pred.walkthrough,
        # changes_in_tabular_description is the changes in tabular description given to the system
        changes_in_tabular_description=pred.changes_in_tabular_description,
    )
    # The Rating is the average of the walkthrough and changes in tabular description ratings
    return (
        evaluator.rating_walkthrough + evaluator.rating_changes_in_tabular_description
    ) / 2


def SummarizerMetricwithgt(gold, pred, trace=None):
    """
    Wrapper for the SummarizerEvaluatorWithGT
    """
    alignment_criterion = """How aligned are the fields **walkthrough_predicted** and 
    **changes_in_tabular_description_predicted** with the **walkthrough_ground_truth** and 
    **changes_in_tabular_description_ground_truth**?"""
    evaluator = dspy.TypedPredictor(SummarizerEvaluatorWithGT)(
        # criterion is the alignment criterion
        criterion=alignment_criterion,
        # file_diff is the file diff given to the system
        file_diff=gold.file_diff,
        # walkthrough_ground_truth is the walkthrough given to the system
        walkthrough_ground_truth=gold.walkthrough,
        # walkthrough_predicted is the walkthrough given to the system
        walkthrough_predicted=pred.walkthrough,
        # changes_in_tabular_description_ground_truth is the changes in tabular description given to the system
        changes_in_tabular_description_ground_truth=gold.changes_in_tabular_description,
        # changes_in_tabular_description_predicted is the changes in tabular description given to the system
        changes_in_tabular_description_predicted=pred.changes_in_tabular_description,
    )
    # The Rating is the average of the walkthrough and changes in tabular description ratings
    return (
        evaluator.rating_walkthrough + evaluator.rating_changes_in_tabular_description
    ) / 2
