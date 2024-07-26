from engine.rule_factory import RuleFactory
from rules.test_rule import TestRuleData


def create_factory() -> RuleFactory:
    rules = [
        TestRuleData('test_rule')
    ]
    return RuleFactory(rules, None)


if __name__ == '__main__':
    factory = create_factory()
    factory.load_rules()
    print(factory.rules)
