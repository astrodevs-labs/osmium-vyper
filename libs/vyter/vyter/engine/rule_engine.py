
from typing import List
from ..types.file import File
from .rule_factory import RuleFactory
from ..types.rule import Rule
from ..types.diagnostic import Diagnostic

class RuleEngine:
    def __init__(self, files: List[File], factory: RuleFactory):
        self.rules: List[Rule] = factory.load_rules()
        self.files = files

    def diagnose(self) -> List[Diagnostic]:
        diags = []
        for file in self.files:
            for rule in self.rules:
                for diag in rule.diagnose(file):
                    diags.append(diag)
        return diags


