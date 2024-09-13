from typing import List
from ..types import diagnostic
from ..types import rule


@rule.rule(
    severity = rule.Severity.ERROR,
    description = "E005: File should not have a shebang.",
    data = {}
)
class NoShebang(rule.Rule):
    def diagnose(self, file) -> List[diagnostic.Diagnostic]:
        file_content = file.get_content()
        if file_content.startswith("#!"):
            return [diagnostic.Diagnostic(
                    line = 1,
                    column = 1,
                    message = f"E005: File should not have a shebang."
                    )]
        return []
