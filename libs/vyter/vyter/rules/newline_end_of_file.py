from typing import List
from ..types import diagnostic
from ..types import rule


@rule.rule(
    severity = rule.Severity.WARNING,
    description = "E004: File should end with a newline.",
    data = {}
)
class NewlineEOF(rule.Rule):
    def diagnose(self, file) -> List[diagnostic.Diagnostic]:
        file_content = file.get_content()
        lines = file_content.split("\n")
        if lines[-1] != "\n" or lines[-1] != "\r\n":
            return [diagnostic.Diagnostic(
                    line = len(lines),
                    column = len(lines[-1]),
                    message = f"E004: File did not end with a newline."
                    )]
        return []
