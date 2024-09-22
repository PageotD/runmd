# -----------------------------------------------------------------------------
# Copyright (c) 2024 Damien Pageot.
#
# This file is part of Your Project Name.
#
# Licensed under the MIT License. You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
# -----------------------------------------------------------------------------

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
from .commands import CmdNames, create_parser
from .config import get_configuration
from .history import load_history, print_history, update_history, write_history
from .process import list_command, process_markdown_files, run_command, show_command
from .vault import TextFileVault


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

    if args.command == CmdNames.HISTCMD:
        if args.id:
            oldcmd = history[int(args.id)]["command"].split(" ")
            # Reparse
            parser = create_parser()
            args = parser.parse_args(oldcmd[1:])
        elif args.clear:
            history = []
        else:
            print_history(history)

    if args.command == CmdNames.VAULTCMD.value:
        mdvault = TextFileVault()
        if args.decrypt:
            mdvault.decrypt_file(args.decrypt[0], args.outfile[0])
        elif args.encrypt:
            mdvault.encrypt_file(args.encrypt[0], args.outfile[0])

    if args.command in [
        CmdNames.RUNCMD.value,
        CmdNames.SHOWCMD.value,
        CmdNames.LISTCMD.value,
    ]:
        blocklist = process_markdown_files(args.file, config)

        if args.command == CmdNames.RUNCMD.value and (args.blockname or args.tag):
            # Convert list of 'KEY=value' strings to a dictionary of environment variables
            env_vars = {
                key: value for env in args.env for key, value in [env.split("=", 1)]
            }
            success = run_command(blocklist, args.blockname, args.tag, config, env_vars)
            history = update_history(history, histsize, usercmd, success)

        elif args.command == CmdNames.SHOWCMD.value and args.blockname:
            show_command(blocklist, args.blockname)

        elif args.command == CmdNames.LISTCMD.value:
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
    parser = create_parser()  # cliargs()
    args = parser.parse_args(command_line)

    # Handle case where no command is provided
    if args.command is None:
        parser.print_help()
    else:
        execute_command(args, config)


if __name__ == "__main__":
    main()
