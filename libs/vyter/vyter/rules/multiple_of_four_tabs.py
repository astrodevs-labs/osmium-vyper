from typing import List
from ..types import diagnostic
from ..types import rule


@rule.rule(
    severity = rule.Severity.WARNING,
    description = "E003: Ensure all indents are a multiple of 4 spaces.",
    data = {}
)
class MultipleOfFourTabs(rule.Rule):
    def diagnose(self, file) -> List[diagnostic.Diagnostic]:
        file_content = file.get_content()
        lines = file_content.split("\n")
        diagnostics = []
        for i, line in enumerate(lines):
            nb_tabs = 0
            for char in line:
                if char != ' ' and char != '\t':
                    break
                nb_tabs += 1
            if nb_tabs % 4 != 0:
                diagnostics.append(diagnostic.Diagnostic(
                    line = i + 1,
                    column = 1,
                    message = f"E003: Ensure all indents are a multiple of 4 spaces."
                    )
                )
        return diagnostics
