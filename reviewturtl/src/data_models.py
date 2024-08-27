from pydantic import BaseModel
from typing import Optional
from enum import Enum


class NodeContext(BaseModel):
    module: str
    file_path: str
    file_name: str
    struct_name: Optional[str]
    snippet: str


class ExtractedNode(BaseModel):
    name: str
    signature: str
    code_type: str
    docstring: Optional[str]
    line: int
    line_from: int
    line_to: int
    context: NodeContext
    node: dict  # Assuming node is a dictionary, adjust if necessary


class IndexingMode(str, Enum):
    READ_FROM_FILE = "read_from_file"
    PARSE_FROM_FILE = "parse_from_file"
