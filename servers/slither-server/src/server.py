import urllib.parse
import os
import subprocess
from pygls import server
import lsprotocol.types as lsp

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
    vulnerabilities = parse_slither_out(file_path, workspace)
    if not vulnerabilities:
        print("No Vulnerabilities found")
        with open("test.txt", "w", encoding="utf-8") as f:
            f.write("No Vulnerabilities found")
            f.close()
    else:
        print("Vulnerabilities found:")
        with open("test.txt", "w", encoding="utf-8") as f:
            f.write("Vulnerabilities found")
            f.close()
        for vulnerability in vulnerabilities:
            print(vulnerability)

def exec_slither(uri, workspace):
    try:
        process = subprocess.Popen(
            ["slither", uri, "--json", "result.json"],
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
    results = []

    process = exec_slither(uri, workspace)
    if not process:
        return results

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        handle_slither_error(uri, workspace, stderr)
        return stderr

    # Parse the terminal output directly
    vulnerabilities = parse_terminal_output(stdout)
    results.extend(vulnerabilities)

    return results

def parse_terminal_output(output):
    results = []
    lines = output.splitlines()
    for line in lines:
        if "sends eth to arbitrary user" in line or \
           "incorrect ERC20 function interface" in line or \
           "ignores return value" in line or \
           "lacks a zero-check on" in line or \
           "Low level call" in line:
            results.append(line)
    return results

def handle_slither_error(uri, workspace, err_output):
    print(f"Vulnerabilities found: {err_output}")

server.start_io()
