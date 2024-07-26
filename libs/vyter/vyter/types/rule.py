from typing import List
from types.diagnostic import Diagnostic


class Rule:
    def __init__(self, id, severity, data):
        self.id = id
        self.severity = severity
        self.data = data

    def diagnose(file, files) -> List[Diagnostic]:
        pass
    
    def get_documentation():
        pass


