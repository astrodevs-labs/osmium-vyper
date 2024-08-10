"""lsp server"""

import urllib.parse
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

    with open(file_path, "r", encoding="utf-8") as file_saved:
        content = file_saved.read()
        file_saved.close()

    with open("test.txt", "w", encoding="utf-8") as f:
        f.write(content)
        f.close()

server.start_io()
