import argparse
import os
import json
import subprocess
import re

from .config import load_config, validate_config, get_default_config_path, copy_config
from .process import process_markdown_files, list_command, show_command, run_command

def main(command_line=None) -> None:
    """
    Main function to parse command-line arguments and execute corresponding actions.

    Args:
        command_line (list, optional): List of command-line arguments. If None, uses sys.argv.
    """

    # Create the top-level parser
    parser = argparse.ArgumentParser(prog='runmd', description='A tool to manage and process code blocks in Markdown files.')

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for the 'run' command
    run_parser = subparsers.add_parser('run', help='Run code blocks in the source file')
    run_parser.add_argument('blockname', nargs='?', default=None, help='Name of the code block to run or "all" to run all blocks')
    run_parser.add_argument('--env', nargs='*', default=[], help='Environment variables to set during execution')
    run_parser.add_argument('--file', nargs='?', default=None, help='Path to the markdown file to process')

    # Subparser for the 'show' command
    show_parser = subparsers.add_parser('show', help='Show code blocks from the source file')
    show_parser.add_argument('blockname', nargs='?', help='Name of the code block to show')
    show_parser.add_argument('--file', nargs='?', default=None, help='Path to the markdown file to process')

    # Subparser for the 'list' command
    list_parser = subparsers.add_parser('list', help='List code blocks in the source file')
    list_parser.add_argument('tag', nargs='?', help='Optional tag to filter the list of code blocks')
    list_parser.add_argument('--file', nargs='?', default=None, help='Path to the markdown file to process')

    # Parse the command-line arguments
    args = parser.parse_args(command_line)

    # Load configuration file
    config_path = get_default_config_path()
    if not os.path.exists(config_path):
        copy_config()
    config = load_config(config_path)

    # Validate configuration
    validate_config(config)

    # Get code block list
    if args.command in ['run', 'show', 'list']:
        blocklist = process_markdown_files(args.file, config)

    # Handle run command
    if args.command == 'run' and args.blockname:
        # Convert list of 'KEY=value' strings to a dictionary
        env_vars = {}
        for env in args.env:
            key, value = env.split('=', 1)
            env_vars[key] = value
        #
        run_command(blocklist, args.blockname, config, env_vars)

    # Handle list command
    elif args.command == 'list':
        list_command(blocklist)
    
    # Handle show command
    elif args.command == 'show' and args.blockname:
        show_command(blocklist, args.blockname)

    # Handle case where no command is provided
    elif args.command is None:
        parser.print_help()

    if args.command in ['run', 'show'] and not args.blockname:
        print("Error: You must provide a code block name or 'all' to run/show.")

if __name__ == "__main__":
    main()
