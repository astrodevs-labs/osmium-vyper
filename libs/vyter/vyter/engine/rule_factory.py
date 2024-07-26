import json
from typing import List
from types.rule import Rule
from types.rule_data import RuleData

class RuleFactory:
    def __init__(self, rules_data: List[RuleData], config_file = None):
        self.rules_data = rules_data
        self.rules: List[Rule] = []
        self.config_file = config_file
    
    def register_rule(self, rule: RuleData):
        self.rules_data[rule.id] = rule

    def create_default_file(self, at):
        self.config_file = at + '/vyter_rules.json'
        with open(self.config_file, 'w') as f:
            f.write('rules:\n\t\t[')
            for rule in self.rules_data:
                f.write(json.dumps(rule.get_json()))
            f.write('\n\t\t]')

    def load_rules(self) -> Rule:
        if not self.config_file:
            self.create_default_file()
        with open(self.config_file) as f:
            data = json.load(f)
            for rule in data:
                if self.rules_data[rule.id]:
                    self.rules.append(self.rules_data[rule.id].create_rule(rule['id'], rule['severity'], rule['data']))
