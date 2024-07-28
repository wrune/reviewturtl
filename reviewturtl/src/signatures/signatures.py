import dspy
from reviewturtl.src.signatures.docstrings import FILE_DIFF_CONTENT_EXPLANATION
from reviewturtl.src.signatures.typed_pydantic_classes import ReviewComments
from typing import List


class SummarizerSignature(dspy.Signature):
    __doc__ = f"""
        {FILE_DIFF_CONTENT_EXPLANATION}
        >> **Specific Instructions**\n
            - The summary should be in English.\n
            - Provide a short and factoid summary with a short description of the cummalative changes in **walkthrough**.\n
            - Then give the summary of changed content per file in a tabular format in markdown table for **changes_in_tabular_description**.\
            - Do not mention which lines have been changed.\n
            - The change summary in the table should be short and concise.\n
        ### Example:\n
        walkthrough:\n
        The method and logic to calculate the area of the triangle has been changed.\n
        changes_in_tabular_description:\n
        | File Name | Changes |
        | --------- | -------- |
        | test.txt  | The method to calculate the area of the triangle has been changed. |
        | test2.txt | The logic to calculate the area of the triangle has been changed. |
    
    """
    file_diff: str = dspy.InputField(
        desc="The diff of the file",
    )
    walkthrough: str = dspy.OutputField(
        desc="The summary of changes made in the PR",
    )
    changes_in_tabular_description: str = dspy.OutputField(
        desc="The Markdown table containing the changes in the file",
    )


class ReviewerSignature(dspy.Signature):
    __doc__ = f"""
        {FILE_DIFF_CONTENT_EXPLANATION}
    >> **Specific Instructions**\n
            - The review should be in English.\n
            - Provide detailed comments for each line change in **line_by_line_comments**.\n
            - Each comment should suggest improvements or corrections to the code changes. Do not include the comments and the lines for which NO CHANGES are required.\n
            - The comments should be concise and to the point.\n
        ### Example:\n
        line_by_line_comments:\n
        [
            \b{{
                "line_range": "40:50",
                "suggested_code_change": "new_code_content",
                "comment": "Consider using a more efficient algorithm for this operation."
            }}\b
        ]
    """
    file_diff: str = dspy.InputField(
        desc="The diff of the file",
    )
    line_by_line_comments: List[ReviewComments] = dspy.OutputField(
        desc="The line by line review for the file",
    )


# Metrics Signatures


class SummarizerEvaluatorWithoutGT(dspy.Signature):
    """Evaluate the quality of a system's answer to a question according to a given criterion."""

    # criterion is the alignment criterion
    criterion: str = dspy.InputField(desc="The evaluation criterion")
    # file_diff is the file diff given to the system
    file_diff: str = dspy.InputField(desc="The File Diff given to the system")
    # walkthrough is the walkthrough given to the system
    walkthrough: str = dspy.InputField(desc="The walkthrough given to the system")
    # changes_in_tabular_description is the changes in tabular description given to the system
    changes_in_tabular_description: str = dspy.InputField(
        desc="The changes in tabular description given to the system"
    )
    # rating_walkthrough is the rating for the walkthrough
    rating_walkthrough: float = dspy.OutputField(
        desc="A float rating between 1 and 5. 5 indicates the walkthrough is perfect and summarized accurately the important parts of the file_diff"
    )
    # rating_changes_in_tabular_description is the rating for the changes in tabular description
    rating_changes_in_tabular_description: float = dspy.OutputField(
        desc="A float rating between 1 and 5. 5 indicates the changes in tabular description is perfect with all the important parts of the file_diff"
    )


class SummarizerEvaluatorWithGT(dspy.Signature):
    """Evaluate the quality of a system's answer to a question according to a given criterion."""

    # criterion is the alignment criterion
    criterion: str = dspy.InputField(desc="The evaluation criterion")
    # file_diff is the file diff given to the system
    file_diff: str = dspy.InputField(desc="The File Diff given to the system")
    # walkthrough is the walkthrough given to the system
    walkthrough_ground_truth: str = dspy.InputField(
        desc="The walkthrough given to the system"
    )
    # walkthrough is the walkthrough given to the system
    walkthrough_predicted: str = dspy.InputField(
        desc="The walkthrough given to the system"
    )
    # changes_in_tabular_description is the changes in tabular description given to the system
    changes_in_tabular_description_ground_truth: str = dspy.InputField(
        desc="The changes in tabular description given to the system"
    )
    changes_in_tabular_description_predicted: str = dspy.InputField(
        desc="The changes in tabular description given to the system"
    )
    # rating_walkthrough is the rating for the walkthrough
    rating_walkthrough: float = dspy.OutputField(
        desc="A float rating between 1 and 5. 5 indicates the walkthrough is perfect and summarized accurately and is closer to the walkthrough_ground_truth"
    )
    # rating_changes_in_tabular_description is the rating for the changes in tabular description
    rating_changes_in_tabular_description: float = dspy.OutputField(
        desc="A float rating between 1 and 5. 5 indicates the changes in tabular description is perfect with all the important parts of the file_diff and is closer to the changes_in_tabular_description_ground_truth"
    )
