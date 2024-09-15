# -----------------------------------------------------------------------------
# Copyright (c) 2024 Damien Pageot.
#
# This file is part of Your Project Name.
#
# Licensed under the MIT License. You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
# -----------------------------------------------------------------------------

"""
Markdown Code Block Processing

This module provides functions for processing Markdown files to handle code blocks. It includes
functionality for extracting code blocks, listing them, displaying their contents, and executing
them based on specified commands.

Functions:
    - process_markdown_files: Process Markdown files in a directory, extracting code blocks based
      on configuration.
    - list_command: List all code blocks along with their names, languages, and other metadata.
    - show_command: Display the content of a specific code block identified by its name.
    - show_code_block: Print the contents of a code block with formatting.
    - run_command: Execute code blocks based on their name or tag, using configuration and
      environment variables.

The `process_markdown_files` function reads Markdown files from a directory and extracts code
blocks using the provided configuration. The `list_command` function lists code blocks with
details, while `show_command` and `show_code_block` are used to display specific code blocks.
The `run_command` function executes code blocks according to the specified criteria and
configuration.

Usage:
    - Use `process_markdown_files` to extract code blocks from Markdown files in a directory.
    - Use `list_command` to print a summary of code blocks.
    - Use `show_command` to print the content of a specific code block.
    - Use `run_command` to execute code blocks, optionally filtered by name or tag.
"""

import configparser
from pathlib import Path

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import get_lexer_by_name

from .config import get_all_aliases
from .parser import parse_markdown
from .runner import run_code_block


def process_markdown_files(
    inputfilepath: str, config: configparser.ConfigParser
) -> list:
    """
    Process all Markdown files in the given directory.

    Args:
        inputfilepath (str): filepath to the markwon file to process
        config (dict): Configuration dictionary containing commands and options.

    Returns:
        list
    """

    # Extract configured languages
    languages = get_all_aliases(config)

    # Initialize blocklist
    blocklist = []

    if inputfilepath is not None and not isinstance(inputfilepath, Path):
        inputfilepath = Path(inputfilepath)

    # Iterate over .md files in the directory and subdirectories
    directory = Path(".")
    for file_path in directory.rglob("*.md"):
        if inputfilepath is None or inputfilepath == file_path:
            try:
                blocklist += parse_markdown(file_path, languages)
            except Exception as e:
                print(f"Error: Failed to parse file '{file_path}' with exception: {e}")
                continue

    return blocklist


def list_command(blocklist: list, tag: str = None) -> None:
    """
    List all code block names along with their language.

    Args:
        blocklist (list): List of dictionaries containing code block information.
        tag (str): Optional tag to filter the blocks.
    """
    name_width = 30
    lang_width = 15
    file_width = 40
    tag_width = 15

    # Header
    header = f"{'NAME'.ljust(name_width)} {'LANG'.ljust(lang_width)} {'FILE'.ljust(file_width)} {'TAG'.ljust(tag_width)}"
    separator = "-" * len(header)

    # Filter blocklist by tag if specified
    filtered_blocks = (
        block for block in blocklist if tag is None or block["tag"] == tag
    )

    # Prepare output lines
    output_lines = [header, separator]
    output_lines.extend(
        f"{block['name'].ljust(name_width)} {block['lang'].ljust(lang_width)} {str(block['file']).ljust(file_width)} {block['tag'].ljust(tag_width)}"
        for block in filtered_blocks
    )

    # Print all at once
    print("\n".join(output_lines))


def show_command(blocklist: list, block_name: str) -> None:
    """
    Handle the 'show' command to display a specific code block.

    Args:
        code_blocks (list): List of code blocks extracted from Markdown.
        block_name (str): Name of the code block to display.

    Returns:
        None
    """
    for block in blocklist:
        if block["name"] == block_name:
            show_code_block(block["name"], block["lang"], block["code"], block["tag"])
            return

    print(f"Error: Code block with name '{block_name}' not found.")


# def show_code_block(name, lang, code, tag):
#     """
#     Display the code block contents.
#     Args:
#         name (str): Name of the code block.
#         lang (str): Language of the code block.
#         code (str): Code block content.
#     """

#     print(f"\033[1m\u26AC {name} ({lang}) {tag}\033[0m")
#     try:
#         for line in code.split("\n"):
#             print(f"\u0020\u0020\033[90m{line}\033[0m")
#     except Exception as e:
#         print(f"Error: Code block '{name}' failed with exception: {e}")


def show_code_block(name, lang, code, tag):
    """
    Display the code block contents with syntax highlighting using Pygments.

    Args:
        name (str): Name of the code block.
        lang (str): Language of the code block.
        code (str): Code block content.
        tag (str): Tag of the code block.
    """

    # print(f"\033[1m\u26AC {name} ({lang}) {tag}\033[0m")
    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = TerminalFormatter()
        highlighted_code = highlight(code, lexer, formatter)

        indented_code = "\n".join(
            "    | " + line for line in highlighted_code.splitlines()
        )
        print(f"\n{indented_code}\n")
    except Exception as e:
        print(f"Error: Code block '{name}' failed with exception: {e}")
        print("Original Code:")
        print(code)


def run_command(
    blocklist: list, block_name: str, tag: str, config: dict, env_vars: dict
) -> None:
    """
    Handle the 'run' command to execute code blocks.

    Args:
        code_blocks (list): List of code blocks extracted from Markdown.
        block_name (str): Name of the code block to run or 'all' to run all.
        tag(str): Name of the tag of the code blocks to execute
        config (dict): Configuration dictionary.

    Returns:
        None
    """

    block_count = 0
    success = True
    blocklist_copy = blocklist.copy()
    # for block in blocklist:
    while blocklist_copy and success:
        block = blocklist_copy.pop(0)
        if block_name == "all" or block_name == block["name"] or tag == block["tag"]:
            if block["exec"]:
                success = run_code_block(
                    block["name"],
                    block["lang"],
                    block["code"],
                    block["tag"],
                    config,
                    env_vars,
                )
                block_count += 1
            else:
                print(
                    f"Error: Language '{block['lang']}' is not configured. Skipping code block '{block['name']}'."
                )
                block_count += 1

    if block_name != "all" and block_count == 0:
        if tag is not None:
            print(f"Error: Code block with tag '{tag}' not found.")
        else:
            print(f"Error: Code block with name '{block_name}' not found.")

    return success
