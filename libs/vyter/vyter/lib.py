from .engine.rule_factory import RuleFactory
from .rules.test_rule import TestRule


def create_factory(file_path: str | None = None) -> RuleFactory:
    rules = [
        TestRule()
    ]
    return RuleFactory(rules, file_path)