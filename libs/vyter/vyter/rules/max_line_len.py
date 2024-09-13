from typing import List
from ..types import diagnostic
from ..types import rule


@rule.rule(
    severity = rule.Severity.WARNING,
    description = "E006: Line should not exceed 79 columns.",
    data = { 'max_len': 79 }
)
class MaxLineLen(rule.Rule):
    def diagnose(self, file) -> List[diagnostic.Diagnostic]:
        file_content = file.get_content()
        lines = file_content.split("\n")
        diagnostics = []
        for i, line in enumerate(lines):
            if len(line) > self.data["max_len"]:
                diagnostics.append(diagnostic.Diagnostic(
                        line = i + 1,
                        column = self.data["max_len"],
                        message = f"E006: Line exceeded {self.data['max_len']} columns."
                        )
                )
        return diagnostics

    def activate_rule(self, rule_data: rule.RuleConfig):
        super().activate_rule(rule_data)
        self.description = f"E006: Line should not exceed {self.data['max_len']} columns."
