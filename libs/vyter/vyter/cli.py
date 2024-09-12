import argparse
from .import lib
from .engine.rule_engine import RuleEngine
from .engine.file_loader import FileLoader


def run() -> None:

    parser = argparse.ArgumentParser(description='Vyter CLI')
    parser.add_argument('root_path', type=str, help='The path of the root directory to analyze', default=".")

    args = parser.parse_args()

    factory = lib.create_factory(args.root_path)
    factory.load_rules()
    file_loader = FileLoader(args.root_path)
    engine = RuleEngine(file_loader.load_files(), factory)
    diags = engine.diagnose()
    for diag in diags:
        print(diag)

