from ast_extractor.ast import filepath_vyper_to_ast
from converter.format2 import convert_ast_to_string
from difflib import unified_diff
import os

def diff_files(original, formatted):
    original_lines = original.splitlines()
    formatted_lines = formatted.splitlines()

    diff = unified_diff(original_lines, formatted_lines, lineterm='')
    return '\n'.join(list(diff))

def format_file(file_path, config, check, raw):
    ast = filepath_vyper_to_ast(file_path)
    if ast is not None:
        formatted_code = convert_ast_to_string(ast, config)
        if check:
            with open(file_path) as reader:
                if raw:
                    return formatted_code
                else:
                    original_code = reader.read()
                    diff = diff_files(original_code, formatted_code)
                    if diff != "":
                        return diff
        else:
            with open(file_path, "w") as writer:
                writer.write(formatted_code)

def format_root(root, config, check, raw):
    output = []
    if os.path.isdir(root):
        for root, _, files in os.walk(root):
            for file in files:
                if file.endswith(".vy"):
                    file_path = os.path.join(root, file)
                    output_file = format_file(file_path, config, check, raw)
                    if output_file is not None:
                        output.append({"filename": file_path, "output": output_file})
    else:
        raise ValueError("Root path is not a directory")
    return output