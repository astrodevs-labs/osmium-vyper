"""lsp server"""

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

server.start_io()
