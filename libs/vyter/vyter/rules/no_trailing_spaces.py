from typing import List
from ..types import diagnostic
from ..types import rule


@rule.rule(
    severity = rule.Severity.WARNING,
    description = "E001: check that lines do not end with trailing whitespace.",
    data = {}
)
class NoTrailingSpaces(rule.Rule):
    def diagnose(self, file) -> List[diagnostic.Diagnostic]:
        file_content = file.get_content()
        lines = file_content.split("\n")
        diagnostics = []
        for i, line in enumerate(lines):
            if line.endswith(' ') or line.endswith('\t'):
                diagnostics.append(diagnostic.Diagnostic(
                    line = i + 1,
                    column = len(line),
                    message = f"E001: check that lines do not end with trailing whitespace."
                    )
                )
        return diagnostics