from typing import List
from ..types import diagnostic
from ..types import rule


@rule.rule(
    severity = rule.Severity.ERROR,
    description = "This is a test rule",
    data = "test"
)
class TestRule(rule.Rule):
    def diagnose(self, file, files) -> List[diagnostic.Diagnostic]:
        return super.diagnose(file, files)

