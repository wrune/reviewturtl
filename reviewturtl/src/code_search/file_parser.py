from reviewturtl.src.data_models import IndexingMode, ExtractedNode
from reviewturtl.src.code_search.utils import extract_nodes
from tree_sitter_language_pack import get_binding, get_language, get_parser
from typing import Optional, List


python_binding = get_binding("python")  # this is an int pointing to the C binding
python_lang = get_language("python")  # this is an instance of tree_sitter.Language
python_parser = get_parser("python")  # this is an instance of tree_sitter.Parser


class TurtlFileParser:
    def __init__(self, mode: Optional[IndexingMode] = None):
        if mode is None:
            self.mode = IndexingMode.READ_FROM_FILE.value
        else:
            self.mode = mode

    def parse_files(self, files: List[str]) -> List[ExtractedNode]:
        """
        Parse the content of the files into structured data
        Args:
            files (List[str]): The files to parse.
        Returns:
            List[ExtractedNode]: The parsed files.
        """
        all_results = []
        for file in files:
            file_path = file["file_path"]
            if not file_path.endswith(".py"):
                # TODO: add support for other file types
                raise ValueError(
                    f"Unsupported file type: {file_path}. Only .py files are supported."
                )
            source_code = file["file_content"].encode("utf-8")
            tree = python_parser.parse(source_code)
            results = extract_nodes(tree, source_code, file_path)
            for result in results:
                result["file_id"] = file["id"]
            all_results.extend(results)
        return all_results
