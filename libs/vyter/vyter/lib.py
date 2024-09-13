import os
from typing import List

from .types.file import File
from .types.diagnostic import Diagnostic
from .engine.rule_factory import RuleFactory
from .engine.rule_engine import RuleEngine
from .rules.max_line_len import MaxLineLen
from .rules.no_shebang import NoShebang
from .rules.multiple_of_four_tabs import MultipleOfFourTabs
from .rules.no_trailing_spaces import NoTrailingSpaces
from .rules.only_space_indents import OnlySpaceIndents
from .rules.newline_end_of_file import NewlineEOF


def create_factory(root_path: str | None = None) -> RuleFactory:
    rules = [
        MaxLineLen(),
        NoShebang(),
        MultipleOfFourTabs(),
        NoTrailingSpaces(),
        OnlySpaceIndents(),
        NewlineEOF(),
    ]
    return RuleFactory(rules, root_path)

def diagnose_file(filepath: str) -> List[Diagnostic]:
    root_path = os.path.dirname(filepath)
    factory = create_factory(root_path)
    file = File(filepath)
    engine = RuleEngine([file], factory)

    return engine.diagnose()