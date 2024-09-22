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

This module defines the command-line interface (CLI) for the 'runmd' tool. It provides
functionality to parse command-line arguments, manage commands, and execute actions based on user
input. The CLI supports commands for running, showing, listing code blocks, and managing command
history.

Functions:
    - create_parser: Create and return the argument parser for the CLI interface.
    - create_commons: Create a parser for arguments that are common across multiple commands.
    - add_run_command: Add the run command to the argument parser.
    - add_list_command: Add the list command to the argument parser.
    - add_show_command: Add the show command to the argument parser.
    - add_hist_command: Add the hist command to the argument parser.

Constants:
    - RUNCMD: Command to run code blocks.
    - SHOWCMD: Command to show code blocks.
    - LISTCMD: Command to list code blocks.
    - HISTCMD: Command to display or clear the command history.

"""

import argparse
from enum import Enum

from . import __version__


class CmdNames(Enum):
    """
    Enum class for command names
    """

    RUNCMD = "run"
    SHOWCMD = "show"
    LISTCMD = "list"
    HISTCMD = "hist"
    VAULTCMD = "vault"


def create_parser() -> argparse.ArgumentParser:
    """
    Create and return the argument parser for the CLI interface.

    Returns:
        argparse.ArgumentParser: The argument parser configured with all subcommands.
    """
    parser = argparse.ArgumentParser(
        prog="runmd",
        description="A tool to manage and process code blocks in Markdown files.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    common_parser = create_commons()

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    add_run_command(subparsers, common_parser)
    add_show_command(subparsers, common_parser)
    add_list_command(subparsers, common_parser)
    add_hist_command(subparsers)
    add_vault_command(subparsers)
    return parser


def create_commons() -> argparse.ArgumentParser:
    """
    Create a parser for arguments that are common across multiple commands.

    Returns:
        argparse.ArgumentParser: The common argument parser.
    """
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "-f",
        "--file",
        nargs="?",
        default=None,
        help="Path to the markdown file to process. If not provided, uses the default file from config.",
    )
    return common_parser


def add_run_command(
    subparsers: argparse._SubParsersAction, common_parser: argparse.ArgumentParser
) -> None:
    """
    Add the run command to the argument parser
    """
    run_parser = subparsers.add_parser(
        CmdNames.RUNCMD.value,
        help="Run code block in the source file",
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


def add_show_command(
    subparsers: argparse._SubParsersAction, common_parser: argparse.ArgumentParser
) -> None:
    """
    Add the show command to the argument parser
    """
    show_parser = subparsers.add_parser(
        CmdNames.SHOWCMD.value,
        help="Show code blocks from the source file",
        parents=[common_parser],
    )
    show_parser.add_argument(
        "blockname",
        nargs="?",
        help="Name of the code block to show",
    )


def add_list_command(
    subparsers: argparse._SubParsersAction, common_parser: argparse.ArgumentParser
) -> None:
    """
    Add the list command to the argument parser
    """
    list_parser = subparsers.add_parser(
        CmdNames.LISTCMD.value,
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


def add_hist_command(subparsers: argparse._SubParsersAction) -> None:
    """
    Add the hist command to the argument parser
    """
    hist_parser = subparsers.add_parser(
        CmdNames.HISTCMD.value,
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


def add_vault_command(subparser: argparse._SubParsersAction) -> None:
    """
    Add the vault command to the argument parser
    """
    vault_parser = subparser.add_parser(
        CmdNames.VAULTCMD.value,
        help="Manage markdown file encryption/decryption",
    )
    vault_group = vault_parser.add_mutually_exclusive_group()
    vault_group.add_argument(
        "--encrypt",
        "-e",
        nargs=1,
        default=None,
        help="Encrypt the markdown file",
    )
    vault_group.add_argument(
        "--decrypt",
        "-d",
        nargs=1,
        default=None,
        help="Decrypt the markdown file",
    )
    vault_parser.add_argument(
        "--outfile",
        "-o",
        nargs=1,
        default=None,
        help="Output file to write the encrypted/decrypted markdown file to",
    )
