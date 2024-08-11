import os
from .config import get_languages
from .parser import parse_markdown
from .runner import run_code_block

def process_markdown_files(directory: str, command: str, block_name: str=None, config: str=None, env_vars: dict=None) -> None:
    """
    Process all Markdown files in the given directory.

    Args:
        directory (str): Directory to scan for Markdown files.
        command (str): Command to run, list, or show code blocks.
        block_name (str, optional): Name of the code block to run or show. If None, processes all.
        config (dict): Configuration dictionary containing commands and options.

    Returns:
        None
    """
    # Validate command input
    if command not in {"ls", "show", "run"}:
        print(f"Error: Invalid command '{command}'. Expected 'ls', 'show', or 'run'.")
        return

    # Extract configured languages
    languages = get_languages(config) if config else []

    # Iterate over files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith(".md"):
            file_path = os.path.join(directory, file_name)
            print(f"\033[0;31m\u26AC\033[0;0m Processing file: {file_path}")

            try:
                code_blocks = parse_markdown(file_path, languages)
            except Exception as e:
                print(f"Error: Failed to parse file '{file_path}' with exception: {e}")
                continue

            # Handle commands
            if command == "ls":
                list_command(code_blocks)
            elif command == "show":
                show_command(code_blocks, block_name)
            elif command == "run":
                run_command(code_blocks, block_name, config, env_vars)

def list_command(code_blocks: tuple) -> None:
    """
    List all code block names along with their language.

    Args:
        code_blocks (list): List of tuples containing code block information.
    """
    print("\033[0;31m\u26AC\033[0;0m Available code block names:")
    for name, lang, _, runnable in code_blocks:
        if runnable:
            print(f"\u0020\u0020\033[0;31m-\033[0;0m {name} ({lang})")
        else:
            print(
                f"\u0020\u0020\033[0;31m-\033[0;0m {name} (\033[0;31m{lang}: not configured\033[0;0m)"
            )

def show_command(code_blocks: list, block_name: str) -> None:
    """
    Handle the 'show' command to display a specific code block.

    Args:
        code_blocks (list): List of code blocks extracted from Markdown.
        block_name (str): Name of the code block to display.

    Returns:
        None
    """
    found = False
    for name, lang, code, _ in code_blocks:
        if name == block_name:
            show_code_block(name, lang, code)
            found = True
            break
    if not found:
        print(f"Error: Code block with name '{block_name}' not found.")

def show_code_block(name, lang, code):
    """
    Display the code block contents.
    Args:
        name (str): Name of the code block.
        lang (str): Language of the code block.
        code (str): Code block content.
    """
    print(f"\n\033[1;33m> Showing: {name} ({lang})\033[0;0m")
    try:
        print(code)
    except Exception as e:
        print(f"Error: Code block '{name}' failed with exception: {e}")
    print(code)

def run_command(code_blocks: list, block_name: str, config: dict, env_vars: dict) -> None:
    """
    Handle the 'run' command to execute code blocks.

    Args:
        code_blocks (list): List of code blocks extracted from Markdown.
        block_name (str): Name of the code block to run or 'all' to run all.
        config (dict): Configuration dictionary.

    Returns:
        None
    """
    if block_name == "all":
        for name, lang, code, runnable in code_blocks:
            if runnable:
                run_code_block(name, lang, code, config, env_vars)
            else:
                print(f"Error: Language '{lang}' is not configured. Skipping code block '{name}'.")
    elif block_name:
        found = False
        for name, lang, code, runnable in code_blocks:
            if name == block_name:
                if runnable:
                    run_code_block(name, lang, code, config, env_vars)
                else:
                    print(f"Error: Language '{lang}' is not configured. Skipping code block '{name}'.")
                found = True
                break
        if not found:
            print(f"Error: Code block with name '{block_name}' not found.")
    else:
        print("Error: You must provide a code block name or 'all' to run.")

