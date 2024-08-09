import argparse
import os
import json
import subprocess
import re

from .config import load_config, get_default_config_path, get_languages
from .process import process_markdown_files

def main() -> None:
    """
    Main function to parse arguments and execute commands.
    """
    parser = argparse.ArgumentParser(
        description="Run or list code blocks from Markdown files in the directory."
    )
    parser.add_argument(
        "command",
        choices=["run", "ls", "show"],
        help="Command to run, list or show code blocks.",
    )
    parser.add_argument(
        "name",
        nargs="?",
        help='Name of the code block to run (or "all" to run all code blocks).',
    )
    parser.add_argument(
        "--dir", default=".", help="Directory to scan for Markdown files."
    )
    parser.add_argument(
        "--config", default=None, help="Path to the configuration file."
    )

    args = parser.parse_args()

    if args.command in ["run", "show"] and not args.name:
        print("Error: You must provide a code block name or 'all' to run/show.")
        return

    config_path = args.config if args.config else get_default_config_path()
    config = load_config(config_path)

    process_markdown_files(args.dir, args.command, args.name, config)


if __name__ == "__main__":
    main()
