from typing import List
from types.diagnostic import Diagnostic
from types.rule import Rule
from types.rule_data import RuleData


class TestRule(Rule):
    def __init__(self, id, severity, data):
        super().__init__(id, severity, data)

    def diagnose(file, files) -> List[Diagnostic]:
        pass

    def get_documentation():
        pass
    
    @staticmethod
    def get_id():
        return "test_rule"

    @staticmethod
    def create_rule(id, severity, data):
        return TestRule(id, severity, data)

    @staticmethod
    def get_json(self):
        return "{'id': " + self.id + "}"


