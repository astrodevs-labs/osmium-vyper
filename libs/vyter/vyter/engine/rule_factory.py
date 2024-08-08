from dataclasses import dataclass
import json
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
            data = config.model_dump_json()
            json.dump(data, f, indent=4)

    def load_rules(self):
        if not self.config_file:
            self.create_default_file()
        with open(self.config_file) as f:
            data = json.load(f)
            config: ConfigFile = ConfigFile.model_validate_json(data)
            print(config)
            for rule_config in config.rules:
                rule: Rule = self.default_rules.filter(lambda r: r.id == rule_config.id).next()
                if rule is None:
                    continue
                rule.activate_rule(rule_config)
                self.rules.append(rule)
