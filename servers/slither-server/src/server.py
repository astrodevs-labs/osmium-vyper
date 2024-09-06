import urllib.parse
import os
import subprocess
from pygls import server
import lsprotocol.types as lsp
import json

server = server.LanguageServer("example-server", "v0.1")

@server.feature(lsp.TEXT_DOCUMENT_COMPLETION)
def completions(params: lsp.CompletionParams):
    """completions test"""
    print("completions")
    items = []
    document = server.workspace.get_document(params.text_document.uri)
    current_line = document.lines[params.position.line].strip()
    if current_line.endswith("hello."):
        items = [
            lsp.CompletionItem(label="world"),
            lsp.CompletionItem(label="friend"),
        ]
    return lsp.CompletionList(is_incomplete=False, items=items)

@server.feature(lsp.TEXT_DOCUMENT_DID_SAVE)
def did_save(params: lsp.DidSaveTextDocumentParams):
    """did save test"""

    file_path = urllib.parse.urlparse(params.text_document.uri).path
    workspace = os.path.dirname(file_path)

    # Use slither to analyze the vulnerabilities
    filtered_data = parse_slither_out(file_path, workspace)
    if not filtered_data:
        with open("test.txt", "w", encoding="utf-8") as f:
            f.write("No Vulnerabilities found")
            f.close()
    else:
        with open("test.txt", "w", encoding="utf-8") as f:
            for data in filtered_data:
                f.write(json.dumps(data))
                f.write("\n")
            f.close()

def exec_slither(uri, workspace):
    try:
        process = subprocess.Popen(
            ["slither", uri, "--exclude", "naming-convention", "--json", "-"],
            cwd=workspace,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"Failed to start Slither: {e}")
        return None

def parse_slither_out(uri, workspace):
    output_dict = {"stdout": "", "stderr": ""}
    
    process = exec_slither(uri, workspace)
    if not process:
        return output_dict

    stdout, stderr = process.communicate()
    output_dict["stdout"] = stdout
    output_dict["stderr"] = stderr  

    if not stdout.strip():
        return []

    filtered_data = parse_json_output(stdout)
    return filtered_data

def parse_json_output(output):
    vulnerabilities = []

    try:
        vulnerabilities_json = json.loads(output)
        detectors = vulnerabilities_json.get("results", {}).get("detectors", [])
        
        for detector in detectors:
            if isinstance(detector, dict):
                impact = detector.get("impact", "Unknown")
                description = detector.get("description", "Unknown")
                for element in detector.get("elements", []):
                    if element.get("type") == "node":
                        filtered_element = {
                            "message": description,
                            "start": element.get("source_mapping", {}).get("start"),
                            "length": element.get("source_mapping", {}).get("length"),
                            "severity": impact
                        }
                        vulnerabilities.append(filtered_element)
            else:
                print(f"Unexpected detector type: {type(detector)}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

    return vulnerabilities


server.start_io()
