from typing import List
from ..types import diagnostic
from ..types import rule


@rule.rule(
    severity = rule.Severity.ERROR,
    description = "This is a B rule",
    data = "test"
)
class BRule(rule.Rule):
    def diagnose(self, file, files) -> List[diagnostic.Diagnostic]:
        print("BRule")
        return []

