import dspy


class SummarizerSignature(dspy.Signature):
    __doc__ = """
    Summarize a document based on the difference between the old and new chunk.\n
    The Summary should be in English.\n
    The summary should be thorough and concise.\n
    Do not provide any instructions to the bot on how to perform the review.\n
    Do not mention that files need a through review or caution about potential issues\n
    The summary should not exceed 500 words.\n
    """
    old_chunk_code: str = dspy.InputField(
        desc="The code of the document",
    )
    new_chunk_code: str = dspy.InputField(
        desc="The code of the document",
    )
    summary: str = dspy.OutputField(
        desc="The summary of the document",
    )
