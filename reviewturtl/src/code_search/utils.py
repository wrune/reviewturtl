import inflection
import re

from typing import Dict, Any

def convert_chunk_to_text(chunk: Dict[str, Any]) -> str:
    """
    Convert a chunk of code to a human-readable text representation.
    Args:
        chunk (Dict[str, Any]): The chunk of code to convert.
    Returns:
        str: The human-readable text representation of the chunk.
    """
    # Convert the 'name' field from camel case to snake case, then to human-readable form
    name = inflection.humanize(inflection.underscore(chunk["name"]))
    
    # Convert the 'signature' field from camel case to snake case, then to human-readable form
    signature = inflection.humanize(inflection.underscore(chunk["signature"]))

    # Initialize the docstring variable
    docstring = ""
    # If a docstring is provided in the chunk, format it appropriately
    if chunk["docstring"]:
        docstring = f"that does {chunk['docstring']} "

    # Extract the module and file name from the context and format them
    context = (
        f"module {chunk['context']['module']} "
        f"file {chunk['context']['file_name']}"
    )
    # If a struct name is provided in the context, convert it to human-readable form and include it
    if chunk["context"]["struct_name"]:
        struct_name = inflection.humanize(
            inflection.underscore(chunk["context"]["struct_name"])
        )
        context = f"defined in struct {struct_name} {context}"

    # Combine all the extracted and formatted pieces into a single text representation
    text_representation = (
        f"{chunk['code_type']} {name} "
        f"{docstring}"
        f"defined as {signature} "
        f"{context}"
    )

    # Split the text representation into tokens, removing any special characters
    tokens = re.split(r"\W", text_representation)
    # Filter out any empty tokens
    tokens = filter(lambda x: x, tokens)
    # Join the tokens back into a single string separated by spaces
    return " ".join(tokens)