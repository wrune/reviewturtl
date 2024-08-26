import inflection
import re
from pathlib import Path
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
        f"module {chunk['context']['module']} " f"file {chunk['context']['file_name']}"
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


def extract_nodes(tree, source_code, source_code_path):
    # TODO: Add support for other file types
    allowed_node_types = ["class_definition", "function_definition"]

    def get_node_text(node):
        """
        Get the text of a node.
        Args:
            node (tree_sitter.Node): The node to get the text from.
        Returns:
            str: The text of the node.
        """
        return source_code[node.start_byte : node.end_byte].decode("utf-8")

    def get_module_name(file_path):
        """
        Get the module name from a file path.
        Args:
            file_path (str): The file path to get the module name from.
        Returns:
            str: The module name.
        """
        module_name = Path(file_path).stem
        return module_name

    def get_struct_name(node):
        """
        Get the struct name from a node.
        Args:
            node (tree_sitter.Node): The node to get the struct name from.
        Returns:
            str: The struct name.
        """
        if node.type == "class_definition":
            definition = get_node_text(node)
            class_name = definition.split()[1].split("(")[0]

            return class_name

        return None

    def get_docstring(node):
        """
        Get the docstring from a node.
        Args:
            node (tree_sitter.Node): The node to get the docstring from.
        Returns:
            str: The docstring.
        """

        def traverse(node):
            is_expression_statement_type = (
                node.parent
                and node.parent.parent
                and node.parent.parent.type == "expression_statement"
            )
            if is_expression_statement_type and node.type == "string_content":
                return get_node_text(node)

            docstring = ""
            for child in node.children:
                child_docstring = traverse(child)
                if child_docstring:
                    docstring += child_docstring

            return docstring

        return traverse(node)

    def get_context(node):
        """
        Get the context from a node.
        Args:
            node (tree_sitter.Node): The node to get the context from.
        Returns:
            dict: The context.
        """
        file_path = source_code_path
        file_name = Path(file_path).name
        module = get_module_name(file_path)
        struct_name = get_struct_name(node)

        return {
            "module": module,
            "file_path": str(file_path),
            "file_name": file_name,
            "struct_name": struct_name,
            "snippet": get_node_text(node),
        }

    root_node = tree.root_node
    results = []

    def traverse(node):
        """
        Traverse a node and extract the relevant information.
        Args:
            node (tree_sitter.Node): The node to traverse.
        """
        if node.type in allowed_node_types:
            results.append(
                {
                    "name": get_node_text(node.child_by_field_name("name")),
                    "signature": get_node_text(node),
                    "code_type": node.type,
                    "docstring": get_docstring(node),
                    "line": node.start_point[0] + 1,
                    "line_from": node.start_point[0] + 1,
                    "line_to": node.end_point[0] + 1,
                    "context": get_context(node),
                    "node": str(node),
                }
            )

        for child in node.children:
            traverse(child)

    # call the traverse function with the root node
    traverse(root_node)
    return results


# if __name__ == "__main__":
#     # Example usage
#     files = [
#         {
#             "file_path": "example1.py",
#             "file_content": """
#     class Node:
#         def __init__(self):
#             self.x = 10
#         def return_type(self):
#             return self.x
#     """,
#         },
#         {
#             "file_path": "example2.py",
#             "file_content": """
#     def hello():
#         return "Hello, world!"
#     """,
#         },
#     ]

#     results = process_files(files)
#     for result in results:
#         print(result)
