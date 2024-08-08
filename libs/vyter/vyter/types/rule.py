from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import re
from typing import List, Union
from pydantic import BaseModel

from . import diagnostic

# Description: This file contains the rule decorator which is used to define a rule for the vyter engine.


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    
    def to_string(self):
        return str(self.value)



class RuleDocumentation(BaseModel):
    id: str
    default_severity: Severity
    info: str
    exemple: str

class RuleConfig(BaseModel):
    id: str
    severity: Severity
    data: Union[object, str]

    

def rule(severity: Severity = Severity.INFO, description: str = "", data: object | str = None, exemple: str = None):
    def rule_decorator(cls):
        cls.severity = severity
        cls.description = description
        cls.data = data
        cls.exemple = exemple
        cls.id = '-'.join([word.lower() for word in re.findall('[A-Z][a-z]*', cls.__name__)])
        cls.is_active = False
        
        def get_documentation(self) -> RuleDocumentation:
            return RuleDocumentation(
                id = self.id,
                default_severity = self.severity, 
                description = self.description,
                exemple = self.exemple
            )
        
        def get_default_config(self) -> RuleConfig:
            return RuleConfig(
                id = self.id,
                severity = self.severity,
                data = self.data
            )

        cls.get_documentation = get_documentation
        cls.get_default_config = get_default_config
        return cls
    
    return rule_decorator


class Rule(ABC):
    def __init__(self):
        pass

    def activate_rule(self, rule_data: RuleConfig = None):
        if rule_data is not None:
            if rule_data.severity is not None:
                self.severity = rule_data.severity
            if rule_data.data is not None:
                self.data = rule_data.data
        self.is_active = True

    @abstractmethod
    def diagnose(self, file, files) -> List[diagnostic.Diagnostic]:
        pass