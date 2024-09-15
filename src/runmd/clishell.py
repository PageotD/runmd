# -----------------------------------------------------------------------------
# Copyright (c) 2024 Damien Pageot.
#
# This file is part of Your Project Name.
#
# Licensed under the MIT License. You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
# -----------------------------------------------------------------------------

import argparse
import cmd
import re
import shlex
import sys

from . import __version__
from .config import get_configuration
from .process import list_command, process_markdown_files, run_command, show_command


class RunMDShell(cmd.Cmd):
    intro = f"Welcome to the RunMD {__version__} CLI shell. Type help or ? to list commands.\n"
    prompt = "\33[0;33mrunmd>\33[0;0m "

    def __init__(self, inputfilepath=None):
        super().__init__()
        self.configuration = get_configuration()
        self.blocklist = []
        if inputfilepath:
            self.inputfilepath = inputfilepath
            self.blocklist = process_markdown_files(inputfilepath, self.configuration)

    def do_list(self, arg):
        """List all code block names along with their language."""
        parser = argparse.ArgumentParser(
            prog="list", description="List available code blocks in the markdown files"
        )
        parser.add_argument(
            "-t",
            "--tag",
            nargs="?",
            default=None,
            help="Optional tag to filter the list of code blocks",
        )
        args = parser.parse_args(shlex.split(arg))
        list_command(self.blocklist, args.tag)

    def do_run(self, arg):
        """Run a specific code block."""
        parser = argparse.ArgumentParser(
            prog="run", description="Run eligible code blocks in the markdown file"
        )
        parser.add_argument(
            "blockname",
            nargs="?",
            default=None,
            help='Name of the code block to run or "all" to run all blocks',
        )
        parser.add_argument(
            "-t",
            "--tag",
            nargs="?",
            default="None",
            help="Execute all code blocks with this tag",
        )
        parser.add_argument(
            "--env",
            nargs="*",
            default=[],
            help="Environment variables to set during execution (e.g., VAR=value)",
        )
        args = parser.parse_args(shlex.split(arg))
        if args.blockname or args.tag:
            env_vars = {
                key: value for env in args.env for key, value in [env.split("=", 1)]
            }
            _ = run_command(
                self.blocklist, args.blockname, args.tag, self.configuration, env_vars
            )

    def do_show(self, arg):
        """Show the content of a specific code block."""
        parser = argparse.ArgumentParser(
            prog="show", description="Show code blocks from the markdown file"
        )
        parser.add_argument(
            "blockname",
            nargs="?",
            help="Name of the code block to show",
        )
        args = parser.parse_args(shlex.split(arg))
        if args.blockname:
            show_command(self.blocklist, args.blockname)

    def do_exit(self, arg):
        """Exit the RunMD shell."""
        print("Exiting...")
        return True  # Returning True exits the shell

    def do_EOF(self, line):
        """Handle EOF (Ctrl+D) to exit the shell."""
        print("Exiting...")
        return True  # Returning True exits the shell

    def postloop(self):
        """Clean up after the shell exits."""
        print("Shell exited.")


def main():
    if len(sys.argv) == 1:
        print(
            f"Welcome to the RunMD {__version__} CLI shell. Type help or ? to list commands."
        )
        print("You must specify a markdown file to process.")
        print("Exiting...")
        return

    RunMDShell(inputfilepath=sys.argv[1]).cmdloop()
