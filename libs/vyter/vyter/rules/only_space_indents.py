from typing import List
from ..types import diagnostic
from ..types import rule


@rule.rule(
    severity = rule.Severity.WARNING,
    description = "E002: Ensure that indents are only spaces, and not hard tabs.",
    data = {}
)
class OnlySpaceIndents(rule.Rule):
    def diagnose(self, file) -> List[diagnostic.Diagnostic]:
        file_content = file.get_content()
        lines = file_content.split("\n")
        diagnostics = []
        for i, line in enumerate(lines):
            for c, char in enumerate(line):
                if char != ' ' and char != '\t':
                    break
                if char == '\t':
                    diagnostics.append(diagnostic.Diagnostic(
                        line = i + 1,
                        column = c + 1,
                        message = f"E002: Indents must be only spaces, and not hard tabs."
                        )
                    )
        return diagnostics