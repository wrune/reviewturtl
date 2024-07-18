import ast
import json
import os

class MethodInfo:
    def __init__(self, name, signature, code_type, docstring, line, line_from, line_to, context):
        self.name = name
        self.signature = signature
        self.code_type = code_type
        self.docstring = docstring
        self.line = line
        self.line_from = line_from
        self.line_to = line_to
        self.context = context

def extract_methods(file_path, base_folder):
    with open(file_path, 'r') as file:
        file_content = file.read()
        node = ast.parse(file_content, filename=file_path)
        lines = file_content.splitlines()

    methods = []

    def visit_node(node, class_name=None):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = child.name
                args = [a.arg for a in child.args.args]
                returns = ast.dump(child.returns) if child.returns else None
                decorators = []
                for d in child.decorator_list:
                    if isinstance(d, ast.Name):
                        decorators.append(d.id)
                    elif isinstance(d, ast.Call) and isinstance(d.func, ast.Name):
                        decorators.append(d.func.id)
                    else:
                        decorators.append(ast.dump(d))
                docstring = ast.get_docstring(child)
                start_lineno = child.lineno
                end_lineno = child.end_lineno
                async_prefix = "async " if isinstance(child, ast.AsyncFunctionDef) else ""
                signature = f"{async_prefix}def {name}({', '.join(args)}) -> {returns if returns else 'None'}"
                code_type = "Method" if class_name else "Function"
                line = start_lineno
                line_from = start_lineno
                line_to = end_lineno
                snippet = '\n'.join(lines[start_lineno-1:end_lineno])

                relative_path = os.path.relpath(file_path, base_folder)
                module = os.path.splitext(relative_path)[0].replace(os.sep, '.')

                context = {
                    "module": module,
                    "file_path": file_path,
                    "file_name": os.path.basename(file_path),
                    "struct_name": class_name if class_name else "unknown",
                    "snippet": snippet
                }

                method_info = MethodInfo(name, signature, code_type, docstring, line, line_from, line_to, context)
                methods.append(method_info.__dict__)
            elif isinstance(child, ast.ClassDef):
                name = child.name
                docstring = ast.get_docstring(child)
                start_lineno = child.lineno
                end_lineno = child.end_lineno
                signature = f"class {name}"
                code_type = "Class"
                line = start_lineno
                line_from = start_lineno
                line_to = end_lineno
                snippet = '\n'.join(lines[start_lineno-1:end_lineno])

                relative_path = os.path.relpath(file_path, base_folder)
                module = os.path.splitext(relative_path)[0].replace(os.sep, '.')

                context = {
                    "module": module,
                    "file_path": file_path,
                    "file_name": os.path.basename(file_path),
                    "struct_name": name,
                    "snippet": snippet
                }

                class_info = MethodInfo(name, signature, code_type, docstring, line, line_from, line_to, context)
                methods.append(class_info.__dict__)

                visit_node(child, class_name=name)
            else:
                visit_node(child, class_name)

    visit_node(node)
    print(f"Extracted {len(methods)} methods from {file_path}")
    return methods

def process_folder(folder_path):
    all_methods = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                methods = extract_methods(file_path, folder_path)
                all_methods.extend(methods)
    return all_methods

def main():
    folder_path = '/Users/abcom/Desktop/github/reviewturtl/reviewturtl'  # Update this to your folder path
    all_methods = process_folder(folder_path)

    with open('/Users/abcom/Desktop/github/reviewturtl/lsp_test/methods.json', 'w') as json_file:
        json.dump(all_methods, json_file, indent=4)

    print(f"Extracted methods from {folder_path} have been saved to methods.json")

if __name__ == "__main__":
    main()