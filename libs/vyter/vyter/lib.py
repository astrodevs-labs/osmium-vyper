from .engine.rule_factory import RuleFactory
from .rules.test_rule import TestRule
from .rules.test_rule2 import BRule


def create_factory(file_path: str | None = None) -> RuleFactory:
    rules = [
        TestRule(),
        BRule()
    ]
    return RuleFactory(rules, file_path)