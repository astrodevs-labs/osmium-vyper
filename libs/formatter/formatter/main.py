import argparse
import os

from rules.config import init_config
from .lib import format_root

def start() -> None:
    parser = argparse.ArgumentParser(description='Vyper Formatter')
    parser.add_argument('--root', type=str, help="The project's root path to format\n\nBy default root of the current working directory", default=".")
    parser.add_argument('--check', action='store_true', help="Run in 'check' mode.\n\nExits with 0 if input is formatted correctly. Exits with 1 if formatting is required", default=False)
    parser.add_argument('--raw', action='store_true', help="In 'check' and stdin modes, outputs raw formatted code instead of the diff", default=False)
    parser.add_argument('--config', type=str, help="Path to the configuration file\n\nBy default search for a `vyfmt.toml` inside the defined root", default=None)
    args = parser.parse_args()

    # Read root directory and check if it exists
    if not os.path.exists(args.root):
        print(f"Error: Root path '{args.root}' does not exist")
        exit(1)

    config = init_config(args.root, args.config)
    output = format_root(args.root, config, args.check, args.raw)

    if args.check:
        if len(output) != 0:
            for file in output:
                print(file["filename"])
                print(file["output"])
                print()
            exit(1)
        else:
            exit(0)