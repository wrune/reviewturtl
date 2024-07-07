import dspy


class SummarizerSignature(dspy.Signature):
    __doc__ = """
        >> **General Instructions**\n
        This **file_diff_content** represents changes made to files in a version control system, such as Git.\n

        **Interpretation of the diff:**\n

        1. **File Information**:\n
            - Each section of the diff corresponds to a specific file.\n
            - The header of each section indicates the file path and the type of change (modification, addition, or deletion).\n

        2. **Change Types**:\n
            - **Modification**: Changes made to an existing file.\n
            - **Addition**: A new file has been created.\n
            - **Deletion**: An existing file has been removed.

        3. **File Hashes**:\n
            - The old and new file hashes represent the state of the file before and after the changes.\n
            - A hash of `0000000` typically indicates that the file did not exist previously (in the case of a new file).\n

        4. **Line Changes**:\n
            - Lines starting with `-` indicate content that was removed or replaced.\n
            - Lines starting with `+` indicate new content that was added.\n
            - Context lines (without `-` or `+`) provide additional information to understand the changes in the surrounding lines.\n

        **How to Interpret the Diff**:\n
        - The diff output is divided into sections, each representing changes to a specific file.\n
        - The lines prefixed with `-` and `+` show the exact changes made to the file content.\n
        - The context lines help in understanding the modifications in the context of the surrounding code or text.

            This diff helps in understanding what changes were made to the files, which lines were added, removed, or modified, and provides a clear view of the modifications in the repository.\n
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
