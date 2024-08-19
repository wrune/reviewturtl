import dspy
from reviewturtl.src.signatures.docstrings import FILE_DIFF_CONTENT_EXPLANATION
from reviewturtl.src.signatures.typed_pydantic_classes import ReviewComments
from typing import List, Dict, Any


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
        desc="The diff of the file to be reviewed",
    )
    file_content: str = dspy.InputField(
        desc="The content of the file",
    )
    line_by_line_comments: List[ReviewComments] = dspy.OutputField(
        desc="The line by line review for the file. Don't include the lines for which NO CHANGES are required.",
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


class CodeSearchSignature(dspy.Signature):
    __doc__ = """
INSTRUCTIONS TO FOLLOW\n
>>> FOR THE PROVIDED **search_query** answer it using the given **context_related_to_search_query**\n
>>> USE **context_related_to_search_query** PROVIDED to ANSWER the **search_query** ONLY IF YOU THINK IT IS RELEVANT\n
>>> RETURN YOUR ANSWER IN A MARKDOWN FORMAT\n
>>> DO NOT MENTION YOUR THOUGHTS IN THE ANSWER\n
>>> MAKE THIS ANSWER PRESENTABLE AS YOU ARE DIRECTLY COMMUNICATING WITH THE USER.\n
>>> GIVE REFERENCES TO THE FILES WHICH HAVE BEEN USED TO GENERATE THE ANSWER.\n
>>> BE VERBOSE AND THOROUGH IN YOUR ANSWER\n
"""
    search_query: str = dspy.InputField(desc="The search query")
    context_related_to_search_query: str = dspy.InputField(
        desc="The context related to search query"
    )
    response_for_search_query: str = dspy.OutputField(
        desc="The response for the search query using the provided context"
    )


class ReactSignature(dspy.Signature):
    __doc__ = """
    INSTRUCTIONS TO FOLLOW\n
    >>> Available agents are the agents that are available to answer the query. They are in a dictionary format with the key as the agent name and the value as the agent description\n
    >>> Think step by step on what agents are best suited to answer the query\n
    >>> Choose the best agents (can be more than one) to answer the query\n
    >>> Return the agents in a list\n
    """
    conversation_history: str = dspy.InputField(desc="The conversation history so far")
    query: str = dspy.InputField(
        desc="The latest user query based on which the agent is to be chosen"
    )
    available_agents: Dict[str, str] = dspy.InputField(
        desc="The Dictionary of available agents with the agent name as the key and the agent description as the value"
    )
    agents_to_use: List[str] = dspy.OutputField(desc="The List of agents to use")


class FindArgumentsForAgent(dspy.Signature):
    __doc__ = """
    INSTRUCTIONS TO FOLLOW\n
    Given the context , agent being used and the arguments to find for the agent find the arguments required for the agent being used
    >>> 
    """
    context: Dict[str, str] = dspy.InputField(
        desc="The context whatever is provided to be used for finding the arguments. There maybe lot of context provided to you be mindful of what agent is being used and what arguments are required for that agent"
    )
    agent_being_used_with_desc: Dict[str, str] = dspy.InputField(
        desc="The agent being used with the agent name and the agent description"
    )
    arguments_to_find: List[str] = dspy.InputField(
        desc="The arguments to find for the agent"
    )
    args_with_values: Dict[str, str] = dspy.OutputField(
        desc="The mapping of the arguments to the agent with key as the argument name and value as the argument value"
    )


class FinalResponseConstructor(dspy.Signature):
    __doc__ = """
    INSTRUCTIONS TO FOLLOW\n
    >>> Available agents are the agents that are available to answer the query. They are in a dictionary format with the key as the agent name and the value as the agent description\n
    >>> All the prediction objects from the agents are provided to you\n
    >>> Construct the final response to the query using the prediction objects from the agents\n
    >>> Return the final response in a markdown format\n
    """
    conversation_history: str = dspy.InputField(desc="The conversation history so far")
    query: str = dspy.InputField(
        desc="The latest user query based on which the agent is to be chosen"
    )
    available_agents: Dict[str, str] = dspy.InputField(
        desc="The Dictionary of available agents with the agent name as the key and the agent description as the value"
    )
    all_prediction_objects: Dict[str, Any] = dspy.InputField(
        desc="This is a dictionary of agents with the agent name as the key and the prediction object from the agent as the value"
    )
    final_response: str = dspy.OutputField(desc="The final response to the query")

class QueryRewriterSignature(dspy.Signature):
    __doc__ = """
    A signature for query rewriting functionality.

    This class defines the input and output fields for a query rewriter,
    which takes into account the conversation history to improve search results.

    Attributes:
        conversation_history (str): The conversation history as a string.
        query (str): The original search query.
        rewritten_query (str): The rewritten search query.
    """
    conversation_history: str = dspy.InputField(desc="The conversation history as a string")
    query: str = dspy.InputField(desc="The original search query")
    rewritten_query: str = dspy.OutputField(desc="The rewritten search query")
