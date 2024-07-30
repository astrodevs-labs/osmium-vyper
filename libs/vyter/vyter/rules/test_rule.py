from typing import List
from vyter.types.diagnostic import Diagnostic
from vyter.types.rule import Rule, Severity, rule


@rule(
    severity = Severity.ERROR,
    description = "This is a test rule",
    data = "test"
)
class TestRule(Rule):
    def diagnose(self, file, files) -> List[Diagnostic]:
        return super.diagnose(file, files)

