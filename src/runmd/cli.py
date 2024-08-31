"""
Command-Line Interface for the 'runmd' CLI Tool

This module defines the command-line interface (CLI) for the 'runmd' tool. It provides functionality to parse command-line arguments, manage commands, and execute actions based on user input. The CLI supports commands for running, showing, listing code blocks, and managing command history.

Functions:
    - cliargs: Create and return the argument parser for the CLI tool.
    - execute_command: Execute the appropriate command based on parsed arguments and configuration.
    - main: Main entry point for the CLI tool that handles argument parsing, configuration loading, and command execution.

Constants:
    - RUNCMD: Command to run code blocks.
    - SHOWCMD: Command to show code blocks.
    - LISTCMD: Command to list code blocks.
    - HISTCMD: Command to display or clear the command history.

This module integrates with the configuration and history modules to provide a complete CLI experience, allowing users to manage code blocks within Markdown files and track their command history.
"""

import argparse
import configparser
import os
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .config import get_configuration
from .history import print_history, load_history, update_history, write_history
from .process import list_command, process_markdown_files, run_command, show_command

RUNCMD = "run"
SHOWCMD = "show"
LISTCMD = "list"
HISTCMD = "hist"


def cliargs() -> argparse.ArgumentParser:
    """
    Create and return the argument parser for the CLI tool.

    This function defines the structure of the available commands, including their arguments,
    and returns the configured argument parser.

    Returns:
        argparse.ArgumentParser: The argument parser configured with all subcommands.
    """
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        prog="runmd",
        description="A tool to manage and process code blocks in Markdown files.",
    )

    # Argument to show current version
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Common arguments for all subparsers
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "-f",
        "--file",
        nargs="?",
        default=None,
        help="Path to the markdown file to process. If not provided, uses the default file from config.",
    )

    # Subparser for the 'run' command
    run_parser = subparsers.add_parser(
        RUNCMD,
        help="Run code blocks in the source file",
        parents=[common_parser],
    )
    run_parser.add_argument(
        "blockname",
        nargs="?",
        default=None,
        help='Name of the code block to run or "all" to run all blocks',
    )
    run_parser.add_argument(
        "-t",
        "--tag",
        nargs="?",
        default=None,
        help="Execute all code blocks with this tag",
    )
    run_parser.add_argument(
        "--env",
        nargs="*",
        default=[],
        help="Environment variables to set during execution (e.g., VAR=value)",
    )

    # Subparser for the 'show' command
    show_parser = subparsers.add_parser(
        SHOWCMD,
        help="Show code blocks from the source file",
        parents=[common_parser],
    )
    show_parser.add_argument(
        "blockname",
        nargs="?",
        help="Name of the code block to show",
    )

    # Subparser for the 'list' command
    list_parser = subparsers.add_parser(
        LISTCMD,
        help="List code blocks in the source file",
        parents=[common_parser],
    )
    list_parser.add_argument(
        "-t",
        "--tag",
        nargs="?",
        default=None,
        help="Optional tag to filter the list of code blocks",
    )

    # Subparser for the 'hist' command
    hist_parser = subparsers.add_parser(
        HISTCMD,
        help="Display or manage the runmd command history",
    )
    hist_group = hist_parser.add_mutually_exclusive_group()
    hist_group.add_argument(
        "id",
        nargs="?",
        default=None,
        help="ID of the command to run from history",
    )
    hist_group.add_argument(
        "--clear",
        action="store_true",
        help="Clear the history list",
    )

    return parser


def execute_command(
    args: argparse.Namespace, config: configparser.ConfigParser
) -> None:
    """
    Execute the appropriate command based on parsed arguments.

    This function takes the parsed command-line arguments and the configuration,
    and executes the corresponding action (run, show, or list).

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        config (dict): The configuration object loaded from the config file.
    """
    # Read history
    histsize = config["DEFAULT"].getint("histsize", 100)
    history = load_history()
    usercmd = " ".join(sys.argv)

    if args.command == HISTCMD:
        if args.id:
            oldcmd = history[int(args.id)]["command"].split(" ")
            # Reparse
            parser = cliargs()
            args = parser.parse_args(oldcmd[1:])
        elif args.clear:
            history = []
        else:
            print_history(history)

    if args.command in [RUNCMD, SHOWCMD, LISTCMD]:
        blocklist = process_markdown_files(args.file, config)

        if args.command == RUNCMD and args.blockname:
            # Convert list of 'KEY=value' strings to a dictionary of environment variables
            env_vars = {
                key: value for env in args.env for key, value in [env.split("=", 1)]
            }
            success = run_command(blocklist, args.blockname, args.tag, config, env_vars)
            history = update_history(history, histsize, usercmd, success)

        elif args.command == SHOWCMD and args.blockname:
            show_command(blocklist, args.blockname)

        elif args.command == LISTCMD:
            list_command(blocklist, args.tag)

        else:
            print("Error: You must provide a code block name or 'all' to run/show.")

    # Write history
    write_history(history) 

def main(command_line: Optional[list[str]] = None) -> None:
    """
    Main entry point for the runmd CLI tool.

    This function handles the overall flow of the program. It parses command-line arguments,
    loads and validates the configuration, and delegates the appropriate command action.

    Args:
        command_line (Optional[list[str]]): The command-line arguments. If None, it uses sys.argv.
    """

    # Load and validate configuration
    config = get_configuration()

    # Parse the command-line arguments
    parser = cliargs()
    args = parser.parse_args(command_line)

    # Handle case where no command is provided
    if args.command is None:
        parser.print_help()
    else:
        execute_command(args, config)


if __name__ == "__main__":
    main()
