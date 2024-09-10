import json
from os import write
from typing import List
from pydantic import BaseModel
from ..types.rule import Rule, RuleConfig

class ConfigFile(BaseModel):
    rules: List[RuleConfig]

class RuleFactory:
    def __init__(self, default_rules: List[Rule], config_file: str | None = None):
        self.default_rules: List[Rule] = default_rules
        self.config_file = config_file
        self.rules = []

    def create_default_file(self, at = '.'):
        self.config_file = at + '/vyter_rules.json'
        with open(self.config_file, 'w') as f:
            config: ConfigFile = ConfigFile(rules = list(map(lambda r: r.get_default_config(), self.default_rules)))
            data = config.model_dump_json(indent=4)
            f.write(data)

    def load_rules(self):
        if not self.config_file:
            self.create_default_file()
        with open(self.config_file) as f:
            config: ConfigFile = ConfigFile.model_validate_json(f.read())
            for rule_config in config.rules:
                rule: Rule = list(filter(lambda r: r.id == rule_config.id, self.default_rules))[0]
                if rule is None:
                    continue
                rule.activate_rule(rule_config)
                self.rules.append(rule)
