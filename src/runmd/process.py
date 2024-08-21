import os
from .config import get_all_aliases
from .parser import parse_markdown
from .runner import run_code_block
import configparser

from pathlib import Path

def process_markdown_files(inputfilepath: str, config: configparser.ConfigParser) -> list:
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
                blocklist = parse_markdown(file_path, languages, blocklist)
            except Exception as e:
                print(f"Error: Failed to parse file '{file_path}' with exception: {e}")
                continue
    
    return blocklist

def list_command(blocklist: list, tag: str) -> None:
    """
    List all code block names along with their language.

    Args:
        code_blocks (list): List of tuples containing code block information.
    """
    #print("\033[0;31m\u26AC\033[0;0m Available code block names:")
    # Define column widths
    name_width = 30
    lang_width = 15
    file_width = 40
    tag_width = 15

    # Print header
    print(f"{'NAME'.ljust(name_width)} {'LANG'.ljust(lang_width)} {'FILE'.ljust(file_width)} {'TAG'.ljust(tag_width)}")

    # Print separator
    print("-" * (name_width + lang_width + file_width + tag_width))

    tagsearch = None
    if tag is not None and tag.startswith('@'):
        tagsearch = tag.replace('@', '')

    # Print each block
    for block in blocklist:
        if tagsearch is None or block['tag'] == tagsearch:
            # Convert PosixPath to string for formatting
            file_str = str(block['file'])
            print(f"{block['name'].ljust(name_width)} {block['lang'].ljust(lang_width)} {file_str.ljust(file_width)} {block['tag'].ljust(name_width)}")


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
        if block['name'] == block_name:
            show_code_block(block['name'], block['lang'], block['code'], block['tag'])
            return
    
    print(f"Error: Code block with name '{block_name}' not found.")

def show_code_block(name, lang, code, tag):
    """
    Display the code block contents.
    Args:
        name (str): Name of the code block.
        lang (str): Language of the code block.
        code (str): Code block content.
    """
 
    print(f"\033[1m\u26AC {name} ({lang}) {tag}\033[0m")
    try:
        for line in code.split('\n'):
            print(f"\u0020\u0020\033[90m{line}\033[0m")
    except Exception as e:
        print(f"Error: Code block '{name}' failed with exception: {e}")

def run_command(blocklist: list, block_name: str, tag: str, config: dict, env_vars: dict) -> None:
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
    for block in blocklist:
        if block_name == "all" or block_name == block['name'] or tag == block['tag']:
            if block['exec']:
                run_code_block(block['name'], block['lang'], block['code'], block['tag'],config, env_vars)
                block_count +=1
            else:
                print(f"Error: Language '{block['lang']}' is not configured. Skipping code block '{block['name']}'.")
                block_count +=1
    
    if block_name != "all" and block_count == 0:
        if tag is not None:
            print(f"Error: Code block with tag '{tag}' not found.")
        else:
            print(f"Error: Code block with name '{block_name}' not found.")